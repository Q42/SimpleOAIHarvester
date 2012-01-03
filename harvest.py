
import urllib2, os, sys
from xml.dom import minidom

if len(sys.argv) < 2: raise Exception('API key required')

apikey = sys.argv[1]
url = u"http://www.rijksmuseum.nl/api/oai?apikey=%s&verb=listrecords&set=collectie_online" % apikey
url2 = u"http://www.rijksmuseum.nl/api/oai?apikey=%s&verb=listrecords&resumptiontoken=" % apikey
count = 0
token = ""

def getText(nodelist):
  rc = []
  for node in nodelist:
      if node.nodeType == node.TEXT_NODE:
          rc.append(node.data)
  return ''.join(rc)

def harvest(url):
  print "downloading: " + url
  data = urllib2.urlopen(url)

  # cache the data because this file-like object is not seekable
  cached  = ""
  for s in data:
    cached += s

  dom = minidom.parseString(cached)

  # check for error
  error = dom.getElementsByTagName('error')
  if len(error) > 0:
    errType = error[0].getAttribute('code')
    desc = getText(error[0].childNodes)
    raise Exception(errType + ": " +desc)

  save(cached)

  countRecords = len(dom.getElementsByTagName('record'))

  nodelist = dom.getElementsByTagName('resumptionToken')
  if len(nodelist) == 0: return None, countRecords
  strToken = getText(nodelist[0].childNodes)

  return strToken, countRecords

def save(data):
  filename = str(count) + '.xml'
  print 'saving: ' + filename
  with open(filename, 'w') as f:
    for s in data:
      f.write(s)

try:

  token, countRecords = harvest(url)
  count += countRecords

  while token:
    token, countRecords = harvest(url2 + token)
    count += countRecords


except:
  print "Unexpected error:", sys.exc_info()[0]
  raise
