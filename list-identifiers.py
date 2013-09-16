#! /usr/bin/env python

import argparse
from oai import *

parser = argparse.ArgumentParser(description='OAI ListIdentifiers verb.')
parser.add_argument('baseUrl', help='The baseUrl of the OAI repository.')
parser.add_argument('format', help='The prefix that denotes the metadataFormat to request. Example: \'oai_dc\'')

args = parser.parse_args()

if __name__ == "__main__":
    xml = list_identifiers(args.baseUrl, args.format)
    parsedUrl = parseUrl(args.baseUrl)
    save(xml, parsedUrl.netloc + "-identifiers")
