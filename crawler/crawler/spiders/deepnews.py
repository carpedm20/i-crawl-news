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
    re = "./backup_apple/%s-%s-%s.json" % (company, str(year).zfill(2), month)
    for file_name in glob(re):
        j = json.loads(open(file_name).read())
        for i in j:
            for k in i['sub']:
                yield k['href']
            yield i['href']

class NewsSpider(Spider):
    name = "news"
    allowed_domains = ["google.com", "google.co.kr"]

    def __init__ (self, month=4, year=2013, query="apple"):


        log.msg("[START] %s" % self.base_url, log.INFO)

    def parse(self, response):

