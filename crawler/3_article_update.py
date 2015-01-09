#/usr/bin/python
import json
import codecs
from glob import glob

import goose
g = goose.Goose()

ARTICLE_DIR = "article"

articles = glob("./%s/*-article.json" % ARTICLE_DIR)
articles.sort()

path = "./%s/*-article.json" % (ARTICLE_DIR)
articles = glob(path)

for article in articles:
    print
    print article
    try:
        article_j = json.loads(open(article).read())
    except:
        continue

    for article_i in article_j:
        try:
            text = article_i['text']
        except:
            print "Gotcha",
            try:
                a = g.extract(article_i['href'])
                article_i['text'] = a.cleaned_text
            except:
                article_i['text'] = ""

            if not article_i['text']:
                print "Failed",

    with codecs.open(article, "w", "utf-8") as f:
        json.dump(article_j, f)
