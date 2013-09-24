#!/usr/bin/env python
import argparse, urllib2, os, sys
from oai import *
from urllib2 import *

parser = argparse.ArgumentParser(description='OAI harvester.')
parser.add_argument('baseUrl', help='The baseUrl of the OAI repository.')
parser.add_argument('metadataPrefix', help='The prefix that denotes the desired metadataformat.')
parser.add_argument('--set', '-s', help='A setspec denoting a subset of the dataset.')
parser.add_argument('--interactive', '-i', action="store_true",  help='In interactive mode, you\'ll have to confirm every new batch by pressing ENTER.')

args = parser.parse_args()

count = 0 # keep track of number of records harvested
curToken = ""

def harvest(token=None):
    if token:
        xml = list_records(args.baseUrl, token=token)
        save(xml, "records-" + token)
    else:
        xml = list_records(args.baseUrl, metadataPrefix=args.metadataPrefix, set=args.set)
        save(xml, "records")

    response = Response(xml)
    # print response
    for rec in response.records:
        print "found record: " + rec.localIdentifier

    countRecords = len(xml.findall(".//oai:record", {"oai": "http://www.openarchives.org/OAI/2.0/"}))

    resToken = xml.find(".//oai:resumptionToken", {"oai": "http://www.openarchives.org/OAI/2.0/"})

    if resToken is None: return None, countRecords

    return resToken.text if resToken is not None else None, countRecords

try:
    curToken, countRecords = harvest()
    count += countRecords

    while curToken:
        print "token received: " + curToken

        if args.interactive:
            raw_input('press any ENTER to continue')
        curToken, countRecords = harvest(curToken)
        count += countRecords

    print "no token found."
    print "done"
except (OAIException, HTTPError) as err:
    print err