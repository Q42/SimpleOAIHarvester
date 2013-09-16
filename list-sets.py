#! /usr/bin/env python

import argparse
from xml.dom import minidom
from utils import *

parser = argparse.ArgumentParser(description='OAI ListSets verb.')
parser.add_argument('baseUrl', help='The baseUrl of the OAI repository.')

args = parser.parse_args()
parsedUrl = parseUrl(args.baseUrl)


#import xml.etree.ElementTree as ET


def list_sets(baseUrl):
    url = baseUrl + "?verb=listsets"

    response = request(url)
    print response

    dom = minidom.parseString(response)

    check_errors(dom)
    return dom

if __name__ == "__main__":
    xml = list_sets(args.baseUrl)
    save(xml.toxml(), parsedUrl.netloc + "-sets")
