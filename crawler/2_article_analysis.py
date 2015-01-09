#/usr/bin/python
from glob import glob
from newspaper import Article
import json

ARTICLE_DIR = "article"

articles = glob("./%s/*-article.json" % ARTICLE_DIR)
articles.sort()

companies = ['google','apple','facebook', 'microsoft', 'ibm', 'oracle']
years = range(2010,2015)

month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6, "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

text_count = 0

for company in companies:
    path = "./%s/%s-*-article.json" % (ARTICLE_DIR, company)

    for article in glob(path):
        try:
            article_j = json.loads(open(article).read())
        except:
            continue
        total = 0
        count = 0
        error = 0

        for article_i in article_j:
            total += 1
            try:
                if article_i['text'] == '':
                    count += 1
                else:
                    text_count += 1
            except:
                error += 1
            """for sub in article_i['sub']:
                total += 1
                try:
                    if sub['text'] == '':
                        count += 1
                except:
                    error += 1"""

        print "%s : %s : %s : %s" % (article, total, count, error)

print " Total text : %s" % text_count
