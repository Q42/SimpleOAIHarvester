#! /usr/bin/env python

import argparse
from xml.dom import minidom
from utils import *

parser = argparse.ArgumentParser(description='OAI ListMetadataFormats verb.')
parser.add_argument('baseUrl', help='The baseUrl of the OAI repository.')

args = parser.parse_args()
parsedUrl = parseUrl(args.baseUrl)


#import xml.etree.ElementTree as ET


def list_metadataformats(baseUrl):
    url = baseUrl + "?verb=listmetadataformats"

    response = request(url)
    print response
    #tree = ET.fromstring(response)

    dom = minidom.parseString(response)

    check_errors(dom)
    #code.interact(local=locals())
    return dom

if __name__ == "__main__":
    xml = list_metadataformats(args.baseUrl)
    save(xml.toxml(), parsedUrl.netloc + "-formats")
