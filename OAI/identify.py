#! /usr/bin/env python

import argparse
from xml.dom import minidom
import utils

parser = argparse.ArgumentParser(description='OAI Identify verb.')
parser.add_argument('baseUrl', help='The baseUrl of the OAI repository.')

args = parser.parse_args()
parsedUrl = utils.parseUrl(args.baseUrl)


def identify(baseUrl):
    url = baseUrl + "?verb=identify"

    response = utils.request(url)
    print response

    dom = minidom.parseString(response)
    utils.check_errors(dom)
    return dom

if __name__ == "__main__":
    xml = identify(args.baseUrl)
    utils.save(xml.toxml(), parsedUrl.netloc + "-identify")
