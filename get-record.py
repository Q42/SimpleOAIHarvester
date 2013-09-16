#! /usr/bin/env python

import argparse
from xml.dom import minidom
from utils import *

parser = argparse.ArgumentParser(description='OAI GetRecord verb.')
parser.add_argument('baseUrl', help='The baseUrl of the OAI repository.')
parser.add_argument('identifier', help='The identifier (fully qualified) of the document that you want to retrieve.')
parser.add_argument('format', help='The prefix that denotes the metadataFormat to request. Example: \'oai_dc\'')

args = parser.parse_args()
parseUrl(args.baseUrl)


def get_record(baseUrl, identifier, format):
    url = baseUrl + "?verb=getrecord&identifier=%s&metadataPrefix=%s" % (identifier, format)
    print url

    response = request(url)
    print response

    dom = minidom.parseString(response)
    check_errors(dom)
    return dom


if __name__ == "__main__":
    xml = get_record(args.baseUrl, args.identifier, args.format)
    save(xml.toxml(), args.identifier)
