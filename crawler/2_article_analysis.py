#/usr/bin/python
from glob import glob
from newspaper import Article
import json
import humanize

#ARTICLE_DIR = "backup"

"""company_dict = {'GOOGL':'google',
                'AAPL' :'apple',
                'FB'   :'facebook',
                'IBM'   :'ibm',
                'MSFT'   :'microsoft',
                'avengeers' : 'the avengers movie',
                'frozen' : 'frozen movie',
                'inception' : 'inception movie',
                'knight' : 'the dark knight',
                'JPY': 'yen',
                'KRW': 'korea won',
                'EUR': 'euro' }"""

companies = ['google','apple','facebook', 'microsoft', 'ibm', 'oracle']
ARTICLE_DIR = "article"
#companies = ['euro','yen','yuan', 'korea']
#ARTICLE_DIR = "money"
#companies = ['the dark knight','inception movie','the avengers movie','frozen movie','interstellar movie']
#ARTICLE_DIR = "movie"

articles = glob("./%s/*-article.json" % ARTICLE_DIR)
articles.sort()

#years = range(2008,2015)
years = range(2008,2016)

month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6, "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

text_count = 0

total_error=0
total_document=0

ll = []
for company in companies:
    lll = []
    words = 0
    documents = 0
    for year in years:
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

        total_error += count
        total_document += total
        #print company, year, len(article), total, count
        print company, year, total, count, error+count
        #print "%s : %s : %s : %s" % (len(article), total, count, error)
        #print '%s,' % total,
        lll.append(str(total))
    print "words", humanize.intword(words), ":", words
    print "doc", humanize.intcomma(documents)
    print "words/doc", humanize.intcomma(float(words)/documents)
    ll.append(",".join(lll))
    #print
print ";\n".join(ll)
print " Total text : %s" % text_count
print " Total error: %s" % total_error
print " Total document: %s" % total_document
