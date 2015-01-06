#/usr/bin/python
import os
from glob import glob
import scipy.io as sio
import json

ARTICLE_DIR = "article"
articles = glob("./%s/*-article.json" % ARTICLE_DIR)

companies = ['ibm','oracle','intel','google','apple','microsoft','facebook']
years = range(2010,2015)

month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6, "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12} 

for company in companies:
    for year in years:
        path = "./%s/%s-%s*-article.json" % (ARTICLE_DIR, company, year)
        articles = glob(path)

        indexes = []
        dates = []
        months = []
        names = []
        related = []
        texts = []
        titles = []

        for article in articles:
            article_j = json.loads(open(article).read())

            for idx, article_i in enumerate(article_j):
                try:
                    if article_i['text'] == '':
                        continue
                except:
                    print "Error %s" % article_i['href']
                    continue

                indexes.append(idx)

                date_list = article_i['date'].split()
                month = month_dict[date_list[0]]
                date = int(date_list[1][:-1])

                dates.append(date)
                months.append(month)

                names.append(article_i['name'])
                related.append(int(article_i['related']))
                texts.append(article_i['text'])
                titles.append(article_i['title'])

        data = {'index'   : indexes,
                'dates'   : dates,
                'months'  : months,
                'names'   : names,
                'related' : related,
                'texts'   : texts,
                'titles'  : titles}

        if not os.path.exists('./mat/%s/' % company):
            os.makedirs('./mat/%s/' % company)

        sio.savemat('./mat/%s/%s.mat' % (company, year), data)
