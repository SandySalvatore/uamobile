# -*- coding: utf-8 -*-
from uamobile.scrapers.base import Scraper

class DoCoMoScraper(Scraper):
    url = 'https://www.nttdocomo.co.jp/service/developer/make/content/ip/'

    def do_scrape(self, doc):
        return [str(x.text) for x in doc.xpath('//div[@class="boxArea" and count(preceding-sibling::*)=2]/div/div[@class="section"]/ul[@class="normal txt" and position()=2]/li')]


class EZWebScraper(Scraper):
    url = 'http://www.au.kddi.com/ezfactory/tec/spec/ezsava_ip.html'

    def do_scrape(self, doc):
        res = []
        table1_rows = doc.xpath("""//table[@height="100%" and @summary=""]/tr/td/table[@summary=""]/tr/td/table/tr/td/table/tr/td/table/tr/td/table/tr[@bgcolor="#ffffff"]""")
        for row in table1_rows:
            cols = row.xpath('./td/div[@class="TableText"]//text()')
            res.append(str('%s%s' % (cols[1], cols[2])))
        table2_rows = doc.xpath("""//table[@height="100%" and @summary=""]/tr/td/table[@summary=""]/tr/td/table/tr/td/table/tr/td/table/tr[@bgcolor="#ffffff"]""")
        for row in table2_rows:
            cols = row.xpath('./td/div[@class="TableText"]//text()')
            res.append(str('%s%s' % (cols[1], cols[2])))
        return res


class SoftBankScraper(Scraper):
    url = 'http://creation.mb.softbank.jp/mc/tech/tech_web/web_ipaddress.html'

    def do_scrape(self, doc):
        return [str(x.text.strip()) for x in doc.xpath("//div[@id='contents']/div[@id='contents_sub']/div[@class='right_contents']//table[1]/tr/th")]


class WillcomScraper(Scraper):
    url = 'http://www.willcom-inc.com/ja/service/contents_service/create/center_info/index.html'

    def do_scrape(self, doc):
        res = []
        sep = 0
        for td in doc.xpath("//div[@id='wrapper']/div/div/div/table[@class='plan03']/tr/td"):
            if td.attrib.get('colspan') == "4":
                if '削除' in td.text:
                    break
            else:
                if td.attrib.get('align') == 'center' and td.attrib.get('bgcolor') == 'white':
                    txt = td.text
                    if txt is not None:
                        txt = txt.strip(r'\u0009\u000a\u000d\u0020\u00a0')
                    if txt:
                        res.append(txt)
        return res
