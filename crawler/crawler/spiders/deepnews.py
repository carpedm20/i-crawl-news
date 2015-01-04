# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import log
from scrapy.http import Request
from lxml import html

from time import sleep
from glob import glob
import json
import re

from crawler.items import *
from crawler.config import *

def get_urls(company, year, month):
    urls = []
    re = "./backup/%s-%s-%s.json" % (company, year, month)
    for file_name in glob(re):
        j = json.loads(open(file_name).read())
        for i in j:
            for k in i['sub']:
                urls.append(k['href'])
            urls.append(i['href'])
    return urls

class DeepNewsSpider(Spider):
    name = "deepnews"
    allowed_domains = ["google.com", "google.co.kr"]
    start_urls = []

    def __init__ (self, month=4, year=2013, query="google"):
        self.start_urls = get_urls(query, year, month)

    def parse(self, response):
        article = Article()
        article['html'] = response.body_as_unicode()
        article['url'] = response.url

        log.msg(" ==> " + article['url'], log.INFO)

        yield article
