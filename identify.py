#! /usr/bin/env python

import argparse
from xml.dom import minidom
from utils import *

parser = argparse.ArgumentParser(description='OAI Identify verb.')
parser.add_argument('baseUrl', help='The baseUrl of the OAI repository.')

args = parser.parse_args()
parsedUrl = parseUrl(args.baseUrl)


def identify(baseUrl):
    url = baseUrl + "?verb=identify"

    response = request(url)
    print response

    dom = minidom.parseString(response)
    check_errors(dom)
    return dom

if __name__ == "__main__":
    xml = identify(args.baseUrl)
    save(xml.toxml(), parsedUrl.netloc + "-identify")
