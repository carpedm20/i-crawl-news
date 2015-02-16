#/usr/bin/python
from glob import glob
from newspaper import Article
from news_list import news_list

import progressbar
import json

companies = ['facebook','ibm','microsoft','google','apple']

for company in companies:
    count = 0
    for fname in glob("./bow/%s*.json" % company):
        j=json.loads(open(fname).read())
        for i in j:
            if i['words'] != '':
                count += 1
    print company, count

from collections import Counter


news = []
for fname in glob("./bow/*.json"):
    j=json.loads(open(fname).read())
    news.extend([i['name'] for i in j if i['text'] != ''])

cc = Counter(news)

sort = []
for i in cc.keys():
    sort.append([i, cc[i]])

from operator import itemgetter
sort = sorted(sort, key=itemgetter(1))

for i in sort:
    print i[0], i[1]

BACKUP_DIR = "backup"
DEEP_DIR = "deep_delay"

deeps = glob("./%s/*-deep.json" % DEEP_DIR)
deeps.sort()

for deep in deeps:
    info = deep.replace('-deep.','.').replace(DEEP_DIR, BACKUP_DIR)

    try:
        info_j = json.loads(open(info).read())
        count = len(info_j)
        for info_i in info_j:
            count += len(info_i['sub'])
    except:
        continue

    try:
        deep_j = json.loads(open(deep).read())
        #print deep, ":", len(deep_j)
    except:
        continue

    urls = [info['href'] for info in info_j]
    subs = [sub['href'] for sub in info['sub'] for info in info_j]

    urls += subs

    deep_urls = [deep_i['url'] for deep_i in deep_j]

    print deep, count, ">=", len(deep_j), ':', count >= len(deep_j), ":", len(list(set(urls) - set(deep_urls)))
