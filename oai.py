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

class Response:
    """
    verb (ex ListRecords)
    responseDate
    request
        - baseUrl
        - args
    - record  [for GetRecord]
    - records [for ListRecords]
    - resumptionToken (for list types)
    """
    def __init__(self, xml):
        # print dir(xml)
        self._elements = {}
        for el in xml.findall("*", { "oai" : "http://www.openarchives.org/OAI/2.0/" } ):

            localName = el.tag.split("}")[1]
            self._elements[localName] = el
            print localName
        # print xml
        self.responseDate = self._elements["responseDate"].text
        self.requestVerb = self._elements["request"].attrib["verb"]
        self.requestArgs = self._elements["request"].attrib
        # print self.requestArgs

        elListRecords = xml.find("oai:ListRecords", { "oai" : "http://www.openarchives.org/OAI/2.0/" } )
        elRecords =  elListRecords.findall("oai:record", { "oai" : "http://www.openarchives.org/OAI/2.0/" } )
        self.records = []
        for el in elRecords:
            self.records.append(Record(el))




class Record:
    """


        - [record]
            - header
                - identifier
                - datestamp
            - metadata

    """
    def __init__(self, element):
        self.identifier = element.find("oai:header/oai:identifier", { "oai" : "http://www.openarchives.org/OAI/2.0/" } ).text
        self.localIdentifier = self.identifier.split(":")[2]

