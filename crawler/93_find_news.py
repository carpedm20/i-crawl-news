from glob import glob
from collections import Counter
import json

is_cutoff = False
company = "apple"
word = "nanowerk"
year = "2010"

articles = []
for ffname in glob("./bow/%s-2014-*bow.json" % company):
    print ffname,
    f_year = int(ffname.split("-")[1])

    j = json.loads(open(ffname).read())
    articles.extend(j)

dates = [a['date'] for a in articles]
dates.sort()
dates = list(set(dates))

for date in dates:
    words = []
    for a in articles:
        if a['date'] == date:
            words.extend(a['words'].split())
    count = Counter(words)['decrease']
    count += Counter(words)['decreased']
    count += Counter(words)['decline']
    count += Counter(words)['declined']
    print count,

"""

def find(word="", year="Jan 29, 2014", company="korea won"):
    bows = []

    for ffname in glob("./bow/%s-2014-*bow.json" % company):
        print ffname,
        f_year = int(ffname.split("-")[1])

        j = json.loads(open(ffname).read())
        bows.extend(j)

    count = 0
    articles = []
    sbows = []
    article_dict = {}

    d = {}
    infoname = 'wnew/KRW-250-4000-2014-2014-tfidf-z-train.evw.info'
    with open(infoname) as infile:
        for e, line in enumerate( infile.readlines() ):
            if e > 0:
                token = line.strip().split("\t")[0][1:].strip()
                value = line.strip().split("\t")[1].split()[-2]
                d[token] = float(value)/float(100)
    infoname = infoname.replace('train','test')
    with open(infoname) as infile:
        for e, line in enumerate( infile.readlines() ):
            if e > 0:
                token = line.strip().split("\t")[0][1:].strip()
                value = line.strip().split("\t")[1].split()[-2]
                #value = line.strip().split("\t")[1].split(" ")[-1][:-1]
                d[token] = float(value)/float(100)

    for bow in bows:
        if is_cutoff:
            if bow['name'] not in news_list:
                continue
        try:
            text = bow['words']
        except:
            continue

        for date in range(15,20):
            if "Jan %s, 2014" % date in bow['date']:
                articles.append(bow)
                sbows.extend(bow['words'].split())
                #print text

    count = Counter(sbows)
    sd = {}

    for v, k in count.items():
        try:
            count[v] = d[v]*k
            sd[v] = d[v]
        except:
            del count[v]
    return articles, count, sd

from collections import *
articles, bows, sd = find(word,company)
a=OrderedDict(sorted(sd.items(), key=lambda t: t[1]))
b=OrderedDict(sorted(bows.items(), key=lambda t: t[1]))
"""
"""
from wabbit_wappa import *
vw2 = VW(i='wnew/AAPL-250-4000-2014-2014-tfidf-z-model.evw')

dates = [a['date'] for a in articles]
dates.sort()
dates = list(set(dates))
for d in dates:
    print d
    words = []
    for article in articles:
        if article['date'] == d:
            words.extend(article['words'].split())

    print vw2.get_prediction(words).prediction"""
