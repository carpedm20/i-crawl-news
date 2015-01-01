# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy import log
import re

class NewsSpider(Spider):
    name = "news"
    allowed_domains = ["google.com"]
    start_urls = (
        'https://www.google.co.kr/search?cf=all&ned=us&hl=en&tbm=nws&gl=us&as_q=apple&as_occt=any&as_drrb=b&as_nloc=U.S.&tbs=cdr:1,cd_min:1/1/2010,cd_max:12/31/2010',
    )

    def parse_a(self, selector):
        href = selector.xpath("@href")[0].extract()
        text = selector.xpath("text()")[0].extract()

        return href, text

    def parse(self, response):
        for articles in response.xpath("//li[@class='g']"):
            main_articles = articles.xpath(".//h3/a")

            if len(main_articles) != 1:
                log.msg("Length of main article is not 1", log.WARNING)
            else:
                main = main_articles[0]
                href, text = self.parse_a(main)

                log.msg(" [MAIN] %s (%s)" % (text, href), log.INFO)

            link_sel = sel.extract()

            if re.search('q=(.*)&sa', link_sel):
                link = re.search('q=(.*)&sa', link_sel).group(1)
                log.msg(link, level=log.INFO) 
        pass
