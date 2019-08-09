# -*- coding: utf-8 -*-
import urllib2
from lxml import etree

class Scraper(object):
    # subclass must override this property
    url = None
    encodings = ['utf-8', 'cp932', 'euc-jp']

    def scrape(self):
        stream = self.get_stream()
        content = stream.read()
        for encoding in self.encodings:
            try:
                unicode_content = content.decode(encoding)
            except UnicodeDecodeError:
                continue
        doc = self.get_document(unicode_content)
        return self.do_scrape(doc)

    def get_document(self, unicode_content):
        doc = etree.fromstring(unicode_content, etree.HTMLParser(remove_comments=True))
        return doc

    def get_stream(self):
        return urllib2.urlopen(self.url)

    def do_scrape(self, doc):
        raise NotImplementedError()

