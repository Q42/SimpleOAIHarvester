
import urllib2
from urlparse import urlparse

def request(url):
    data = urllib2.urlopen(url)

    # cache the data because this file-like object is not seekable
    copied = ""
    for s in data:
        copied += s

    return copied

def save(data, filename):
    filename += '.xml'
    filename = filename.replace(":","_")
    print 'saving: ' + filename
    with open(filename, 'w') as f:
        for s in data:
            f.write(s)

def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

def check_errors(dom):
    # check for error
    error = dom.getElementsByTagName('error')
    if len(error) > 0:
        errType = error[0].getAttribute('code')
        desc = getText(error[0].childNodes)
        raise Exception(errType + ": " + desc)

def parseUrl(url):
    parsedUrl = urlparse(url)
    if not parsedUrl.scheme or not parsedUrl.netloc:
        raise Exception("invalid url")
    return parsedUrl

