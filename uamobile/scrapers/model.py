# -*- coding: utf-8 -*-
from uamobile.scrapers.base import Scraper

class EZWebScraper(Scraper):
    url = 'http://www.au.kddi.com/ezfactory/tec/spec/new_win/ezkishu.html'

    def do_scrape(self, doc):
        res = []
        for tr in doc.xpath('//table[@cellspacing="1"]/tr'):
            t = tr.findall('td/div')
            if len(t) >= 2 and t[0].text is not None and t[1].text is not None:
                res.append((t[1].text, str(t[0].text)))
        return res
