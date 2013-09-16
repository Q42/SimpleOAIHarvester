#! /usr/bin/env python

import argparse
from oai import *

parser = argparse.ArgumentParser(description='OAI ListSets verb.')
parser.add_argument('baseUrl', help='The baseUrl of the OAI repository.')

args = parser.parse_args()

if __name__ == "__main__":
    xml = list_sets(args.baseUrl)
    parsedUrl = parseUrl(args.baseUrl)
    save(xml, parsedUrl.netloc + "-sets")
