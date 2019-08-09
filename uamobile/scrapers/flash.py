# -*- coding: utf-8 -*-
import re
from uamobile.scrapers.base import Scraper

class DoCoMoScraper(Scraper):
    url = 'https://www.nttdocomo.co.jp/service/developer/make/content/spec/flash/index.html'

    def do_scrape(self, doc):
        tables = doc.xpath('//table[starts-with(@summary, "Flash")]')

        res = {}
        for table, version in zip(tables, ('1.0', '1.1', '3.0', '3.1')):
            for columns in table.xpath('tr'):
                if len(columns) == 10:
                    span = columns[0].find("span")
                elif len(columns) == 11:
                    span = columns[1].find("span")
                else:
                    continue

                model = span.text.strip()
                matcher = re.match(r'([A-Z]{1,2})-?(\d{1,3}[a-zA-Z\u03bc]+)', model)
                if not matcher:
                    continue

                model = matcher.group(1) + matcher.group(2)
                if model.endswith('\u03bc'):
                    model = model[:-1] + 'myu'

                res[str(model)] = str(version)

        return res


class EZWebScraper(Scraper):
    url = 'http://www.au.kddi.com/ezfactory/tec/spec/new_win/ezkishu.html'

    def get_model(self, name):
        from uamobile.data.model.ezweb import DATA
        for k, v in DATA:
            if v == name:
                return k
        return None

    def do_scrape(self, doc):
        tables = doc.xpath('//table[@width="892"]')
        res = {}
        for table in tables:
            for tr in table.xpath('tr'):
                if tr.attrib.get('bgcolor') == '#e5e5e5':
                    continue

                version = ''.join(tr[13].itertext()).strip()
                if version == '\uff0d':
                    version = None

                model = ''.join(tr[1].itertext()).strip()
                res[str(model)] = str(version)

        return res

class SoftBankScraper(Scraper):
    url = 'http://creation.mb.softbank.jp/mc/terminal/terminal_info/terminal_flash.html'

    def do_scrape(self, doc):
        res = {}
        tables = doc.xpath(r'//div[@id="contents"]//div[@class="right_contents"]//div[@class="terminaltable"]/table')
        for table in tables:
            for tr in table.xpath('tr/td[(@class != "terminalname") and (@class != "hedder")]/..'):
                if len(tr) == 5:
                    models = tr[0].text.strip()
                    g = re.match(r'Flash Lite(?:\u2122|\[TM\])([0-9]+\.[0-9]+)', tr[1].text.strip())
                    if g is not None:
                        version = g.group(1)
                    else:
                        version = None
                    models = models.split('/')
                    for model in models:
                        res[model] = str(version)

        return res
