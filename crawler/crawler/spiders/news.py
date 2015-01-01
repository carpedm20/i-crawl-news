# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import log
from config import SEARCH_URL
from lxml import html
import re

from crawler.items import *

def get_url(min_m, min_d, min_y, max_m, max_d, max_y):
    return SEARCH_URL.format(min_month=min_m,
                             min_date=min_d,
                             min_year=min_y,
                             max_month=max_m,
                             max_date=max_d,
                             max_year=max_y)

class NewsSpider(Spider):
    name = "news"
    allowed_domains = ["google.com"]

    def __init__ (self, month, year):
        url = get_url(month, 1, year, month, 31, year)
        self.start_urls = [url]

        log.msg("[START] %s" % url, log.INFO)

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

        pass
