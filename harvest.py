
import urllib2
from xml.dom import minidom
import sys

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

  token = dom.getElementsByTagName('resumptionToken')
  if len(token) == 0: return None

  return getText(token[0].childNodes)

def save(data):
  filename = str(count) + '.xml'
  print 'saving: ' + filename
  with open(filename, 'w') as f:
    for s in data:
      f.write(s)

token = harvest(url)

while token:
  count += 1
  token = harvest(url2 + token)

