import urllib2
from urlparse import urlparse
import xml.etree.ElementTree as ET

class OAIException(Exception):
    pass

def identify(base_url):
    return request(base_url, {
        "verb" : "identify"
    })

def get_record(base_url, identifier, metadataPrefix):
    return request(base_url, {
        "verb" : "getrecord",
        "metadataprefix" : metadataPrefix,
        "identifier" : identifier
    })

def list_metadataformats(base_url):
    return request(base_url, {
        "verb" : "listmetadataformats"
    })

def list_sets(base_url):
    return request(base_url, {
        "verb" : "listsets"
    })

def list_identifiers(base_url, metadataPrefix):
    return request(base_url, {
        "verb" : "listidentifiers",
        "metadataprefix" : metadataPrefix,
    })

def list_records(base_url, metadataPrefix=None, set=None, token=None):
    if not token:
        args = {
        "verb" : "listrecords",
        "metadataprefix" : metadataPrefix
        }

        if set:
            args["set"] = set

        return request(base_url, args)
    else:
        return request(base_url, {
            "verb" : "listrecords",
            "resumptiontoken": token
    })


def request(baseUrl, params):
    parsedUrl = urlparse(baseUrl)
    if not parsedUrl.scheme or not parsedUrl.netloc:
        raise Exception("invalid url")

    if parsedUrl.query:
        raise Exception("invalid url")

    url = baseUrl + "?"
    for i,(k,v) in enumerate(params.items()):
        url += k + "=" + v
        if i < len(params)-1:
            url += "&"

    print url
    response = urllib2.urlopen(url)
    data = ""
    for s in response:
        data += s

    el = ET.fromstring(data)
    check_errors(el)

    return ET.ElementTree(el)

def save(xml, filename):
    filename += '.xml'
    filename = filename.replace(":","_")
    print 'saving: ' + filename
    ET.register_namespace("", "http://www.openarchives.org/OAI/2.0/")
    ET.register_namespace("oai_dc", "http://www.openarchives.org/OAI/2.0/oai_dc/")

    xml.write(filename, encoding="utf-8", xml_declaration=True)

def check_errors(dom):
    nodes = dom.findall('.//oai:error', { "oai" : "http://www.openarchives.org/OAI/2.0/" } )
    if len(nodes) > 0:
        error = nodes[0]
        raise OAIException(error.attrib['code'] + ": " + error.text)

def parseUrl(url):
    parsedUrl = urlparse(url)
    if not parsedUrl.scheme or not parsedUrl.netloc:
        raise Exception("invalid url")
    return parsedUrl

