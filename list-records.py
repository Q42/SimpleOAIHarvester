#! /usr/bin/env python

import argparse, sys
from urllib2 import HTTPError
from oai import *

parser = argparse.ArgumentParser(description='OAI ListRecords verb.')
parser.add_argument('baseUrl', help='The baseUrl of the OAI repository.')
parser.add_argument('format', help='The prefix that denotes the metadataFormat to request. Example: \'oai_dc\'')
parser.add_argument('--set', '-set', help='A setspec denoting a subset of the dataset.')

args = parser.parse_args()

if __name__ == "__main__":
    print parser.description
    try:
        xml = list_records(args.baseUrl, args.format, set=args.set)
    except (OAIException, HTTPError) as err:
        print err
        sys.exit(1)
    parsedUrl = parseUrl(args.baseUrl)
    save(xml, parsedUrl.netloc + "-records")
