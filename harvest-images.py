import urllib, urllib2, os, sys, re, threading, Queue
from xml.dom import minidom
from retry import *

IMAGE_PATH = 'images'
XML_PATH = 'xml'

# url matchgin regexp from Django
urlPattern = re.compile(
        r'^(?:http|ftp)s?://' # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|' #domain...
        r'localhost|' #localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})' # ...or ip
        r'(?::\d+)?' # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

if len(sys.argv) < 2: raise Exception('API key required')
resumeFile = sys.argv[2] if len(sys.argv) >= 3 else None
apikey = sys.argv[1]

url = u"http://www.rijksmuseum.nl/api/oai/%s/?verb=listrecords&metadataPrefix=oai_dc" % apikey
url2 = u"http://www.rijksmuseum.nl/api/oai/%s/?verb=listrecords&resumptiontoken=" % apikey
count = 0 # keep track of number of records harvested
token = ""

class ThreadUrl(threading.Thread):
  """Threaded Url Grab"""
  def __init__(self, queue):
    threading.Thread.__init__(self)
    self.queue = queue

  def run(self):
    while True:
      imageUrl, imagePath = self.queue.get()

      try:
        retry(urllib.urlretrieve, 3)(imageUrl, imagePath)
      finally:
        self.queue.task_done()


queue = Queue.Queue()
#spawn a pool of threads, and pass them queue instance
for i in range(20):
  t = ThreadUrl(queue)
  #t.setDaemon(True)
  t.start()

def getText(node):
  rc = []
  for child in node.childNodes:
    if child.nodeType == child.TEXT_NODE:
      rc.append(child.data)
  return ''.join(rc)


def harvest(url):
  print "downloading: " + url
  data = retry(urllib2.urlopen, 3)(url)

  # cache the data because this file-like object is not seekable
  cached  = ""
  for s in data:
    cached += s

  dom = minidom.parseString(cached)

  # check for error
  error = dom.getElementsByTagName('error')
  if len(error) > 0:
    errType = error[0].getAttribute('code')
    desc = getText(error)
    raise Exception(errType + ": " +desc)

  save(cached)
  records = dom.getElementsByTagName('record')
  countRecords = len(records)

  for record in records:
    handleRecord(record)

  queue.join()

  nodelist = dom.getElementsByTagName('resumptionToken')
  if len(nodelist) == 0: return None, countRecords
  strToken = getText(nodelist[0])

  return strToken, countRecords

def save(data):
  if not os.path.exists(XML_PATH):
    os.makedirs(XML_PATH)

  filename = str(count) + '.xml'
  print 'saving batch: ' + filename
  filepath = os.path.join(XML_PATH, filename)

  with open(filepath, 'w') as f:
    for s in data:
      f.write(s)

def handleRecord(record):
  retrieveImages(record)

def retrieveImages(record):
  if not os.path.exists(IMAGE_PATH):
    os.makedirs(IMAGE_PATH)

  identifier = getText( record.getElementsByTagName('dc:identifier')[0] )
  formats = [ getText(tag) for tag in record.getElementsByTagName('dc:format') ]
  urls = filter(lambda str: urlPattern.match(str), formats )
  imageUrl = urls[0] + '&100x100'
  imagePath = os.path.join(IMAGE_PATH, identifier +'.jpg')

  #populate queue with data

  queue.put( (imageUrl, imagePath) )


  #print '\tdownloading image:', imagePath
  #urllib.urlretrieve(imageUrl, imagePath)

def resume(filename):
  with open(filename, 'r') as f:
    data = f.read()
     # cache the data because this file-like object is not seekable
    cached  = ""
    for s in data:
      cached += s

    dom = minidom.parseString(cached)

    countRecords = len(dom.getElementsByTagName('record'))

    nodelist = dom.getElementsByTagName('resumptionToken')
    if len(nodelist) == 0: return None, countRecords
    strToken = getText(nodelist[0])

    return strToken, countRecords

try:

  if resumeFile:
      token, countRecords = resume(resumeFile)
      count += int(os.path.basename(resumeFile).split('.')[0]) + countRecords
  else:
    token, countRecords = harvest(url)
    count += countRecords

  #os.exit(0)
  while token:
    token, countRecords = harvest(url2 + token)
    count += countRecords


except:
  print "\n!!!"
  print "Unexpected error"
  print "To resume run this script with the last succesfully harvested file as second paramater:"
  print "python harvest.py <API KEY> <LAST HARVESTED FILE>"
  print "!!!\n"
  raise
