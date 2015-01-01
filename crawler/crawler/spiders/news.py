# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import log
from scrapy.http import Request
from lxml import html

from time import sleep
import re

from crawler.items import *
from crawler.config import *

def get_url(min_m, min_d, min_y, max_m, max_d, max_y, query):
    return SEARCH_URL.format(min_month=min_m,
                             min_date=min_d,
                             min_year=min_y,
                             max_month=max_m,
                             max_date=max_d,
                             max_year=max_y,
                             query=query)

class NewsSpider(Spider):
    name = "news"
    allowed_domains = ["google.com", "google.co.kr"]

    def __init__ (self, month, year, query):
        self.base_url = get_url(month, 1, year, month, 31, year, query)
        self.start_urls = [self.base_url]

        log.msg("[START] %s" % self.base_url, log.INFO)

    def parse_article(self, selector, is_main=True):
        if is_main:
            a = selector.xpath("h3/a")[0]
            info = selector.xpath("div/span")
        else:
            a = selector.xpath("a")[0]
            info = selector.xpath("span")

        href = a.xpath("@href")[0].extract()
        elem = html.fragment_fromstring(a.extract())
        title = elem.text_content()

        if len(info) != 3:
            log.msg("[parse_main_article] Wrong span # : %s" % len(info), log.ERROR)
        name = info[0].xpath("text()")[0].extract()
        date = info[2].xpath("text()")[0].extract()

        if is_main:
            news = MainNews()
            news['sub'] = []
            log.msg("[MAIN] %s (%s)" % (title, href), log.INFO)
        else:
            news = News()
            log.msg("[SUB] %s (%s)" % (title, href), log.INFO)

        news['href'] = href
        news['title'] = title
        news['name'] = name
        news['date'] = date 

        return news

    def parse(self, response):
        for li in response.xpath("//li[@class='g']"):
            divs = li.xpath("./div/div[@class!='_Vmc']")

            main = divs[0]
            main = self.parse_article(main)

            if len(divs) > 1:
                for div in divs[1:]:
                    sub = self.parse_article(div, False)
                    main['sub'].append(sub)

            yield main

        # Check next page
        nav = response.xpath("//div[@id='navcnt']")
        tds = nav.xpath(".//td")

        cur_find = False
        for td in tds:
            if not cur_find:
                classes = td.xpath("@class").extract()
                if len(classes) == 0:
                    continue
                elif classes[0] == "cur":
                    cur_find = True
            else:
                classes = td.xpath("@class").extract()
                if len(classes) == 0:
                    href = td.xpath("a/@href")[0].extract()
                    start = re.findall(r"&start=\d+&", href)[0]
                    start = re.findall(r"\d+",start)[0]

                    sleep(SLEEP_TIME)
                    yield Request(self.base_url+"&start="+start)
                elif classes[0] == "b navend":
                    pass
                break

