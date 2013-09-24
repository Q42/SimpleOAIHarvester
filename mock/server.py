#! /usr/bin/env python

__author__ = 'remcoder'

import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        verb = self.get_argument("verb").lower()
        print "verb:" + verb
        resumptionToken = self.get_argument("resumptiontoken", None)
        if resumptionToken:
            print "token: " + resumptionToken
            resumptionToken = resumptionToken.lower()

        self.set_header("Content-Type", "application/xml")
        print "?? " + str (verb == "listrecords" and resumptionToken)
        if verb == "listrecords" and resumptionToken:
            filename = verb +  "-"+resumptionToken  + ".xml"
        else:
            filename = verb + ".xml"
        print "filename" + filename
        with open(filename) as file:
            self.write(file.read())

if __name__ == "__main__":
    application = tornado.web.Application([
        (r"/", MainHandler),
    ])
    application.listen(8888)
    print "listening on localhost:8888"
    tornado.ioloop.IOLoop.instance().start()
