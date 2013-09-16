#! /usr/bin/env python

import urllib2, os, sys
from xml.dom import minidom
from urlparse import urlparse

if len(sys.argv) < 2: raise Exception('baseUrl required')
baseUrl = sys.argv[1]
parsedUrl = urlparse(baseUrl)
if not parsedUrl.scheme or not parsedUrl.netloc:
    # TODO interpret as local filename
    raise Exception("invalid url")

count = 0 # keep track of number of records harvested
token = ""


def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def list_records(baseUrl):
    url = baseUrl + "?verb=listrecords&metadataPrefix=oai_dc"
    print "downloading: " + url
    data = urllib2.urlopen(url)

    # cache the data because this file-like object is not seekable
    cached = ""
    for s in data:
        cached += s

    dom = minidom.parseString(cached)

    # check for error
    error = dom.getElementsByTagName('error')
    if len(error) > 0:
        errType = error[0].getAttribute('code')
        desc = getText(error[0].childNodes)
        raise Exception(errType + ": " + desc)

    save(cached)

    countRecords = len(dom.getElementsByTagName('record'))

    nodelist = dom.getElementsByTagName('resumptionToken')
    if len(nodelist) == 0: return None, countRecords
    strToken = getText(nodelist[0].childNodes)

    return strToken, countRecords


def save(data):
    filename = str(count) + '.xml'
    print 'saving: ' + filename
    with open(filename, 'w') as f:
        for s in data:
            f.write(s)


def resume(filename):
    with open(filename, 'r') as f:
        data = f.read()
        # cache the data because this file-like object is not seekable
        cached = ""
        for s in data:
            cached += s

        dom = minidom.parseString(cached)

        countRecords = len(dom.getElementsByTagName('record'))

        nodelist = dom.getElementsByTagName('resumptionToken')
        if len(nodelist) == 0: return None, countRecords
        strToken = getText(nodelist[0].childNodes)

        return strToken, countRecords


try:
    token, countRecords = list_records(baseUrl)
    count += countRecords

    # while token:
    #   token, countRecords = harvest(url2 + token)
    #   count += countRecords

except:
    if count > 0:
        print "\n!!!"
        print "Unexpected error"
        print "To resume run this script with the last succesfully harvested file as second paramater:"
        print "python harvest.py <API KEY> <LAST HARVESTED FILE>"
        print "!!!\n"
    raise
