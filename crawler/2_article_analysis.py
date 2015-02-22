#/usr/bin/python
from glob import glob
from newspaper import Article
import json

#ARTICLE_DIR = "backup"
#ARTICLE_DIR = "article"
ARTICLE_DIR = "money"

articles = glob("./%s/*-article.json" % ARTICLE_DIR)
articles.sort()

#companies = ['google','apple','facebook', 'microsoft', 'ibm', 'oracle']
companies = ['euro','yen','yuan', 'korea']
years = range(2010,2015)

month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6, "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

text_count = 0

ll = []
for company in companies:
    lll = []
    words = 0
    documents = 0
    for year in ['2010','2011','2012','2013','2014']:
        path = "./%s/%s*-%s*.json" % (ARTICLE_DIR, company, year)
        #print path

        total = 0
        count = 0
        error = 0

        for article in glob(path):
            try:
                article_j = json.loads(open(article).read())
            except:
                continue

            for article_i in article_j:
                try:
                    if article_i['text'] == '':
                        count += 1
                    else:
                        total += 1
                        documents += 1
                        text_count += 1
                        words += len(article_i['text'].split())
                except:
                    error += 1
                """for sub in article_i['sub']:
                    total += 1
                    try:
                        if sub['text'] == '':
                            count += 1
                    except:
                        error += 1"""

        #print company, year, len(article), total, count
        print company, year, total, count
        #print "%s : %s : %s : %s" % (len(article), total, count, error)
        #print '%s,' % total,
        lll.append(str(total))
    print float(words)/documents
    ll.append(",".join(lll))
    #print
print ";\n".join(ll)
print " Total text : %s" % text_count
