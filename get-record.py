#! /usr/bin/env python

import argparse, sys
from urllib2 import HTTPError
from oai import *

parser = argparse.ArgumentParser(description='OAI GetRecord verb.')
parser.add_argument('baseUrl', help='The baseUrl of the OAI repository.')
parser.add_argument('identifier', help='The identifier (fully qualified) of the document that you want to retrieve.')
parser.add_argument('format', help='The prefix that denotes the metadataFormat to request. Example: \'oai_dc\'')

args = parser.parse_args()

if __name__ == "__main__":
    print parser.description
    try:
        xml = get_record(args.baseUrl, args.identifier, args.format)
    except (OAIException, HTTPError) as err:
        print err
        sys.exit(1)

    save(xml, args.identifier)
