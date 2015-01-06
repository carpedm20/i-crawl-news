#/usr/bin/python
from glob import glob
from newspaper import Article
import json

ARTICLE_DIR = "article"

articles = glob("./%s/*-article.json" % ARTICLE_DIR)
articles.sort()

for article in articles:
    article_j = json.loads(open(article).read())
    total = 0
    count = 0
    error = 0

    for article_i in article_j:
        total += 1
        try:
            if article_i['text'] == '':
                count += 1
        except:
            error += 1
        for sub in article_i['sub']:
            total += 1
            try:
                if sub['text'] == '':
                    count += 1
            except:
                error += 1

    print "%s : %s : %s : %s" % (article, total, count, error)
