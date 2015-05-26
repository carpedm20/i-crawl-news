import json
from collections import Counter

name = 'google'
company = 'GOOGL'
year = '2010'
month = '2'

j=json.loads(open('./bow/%s-%s-%s-bow.json' % (name, year, month)).read())

twords = []
for i in j:
    if i['date'] in ['Feb %s, 2010' % d for d in range(16,23)]:
        twords.extend(i['words'].split())
        print i['title']

counter = Counter(twords)

d = {}
infoname = "wnew/%s-250-4000-%s-%s-tfidf-z-train.evw.info" % (company, year, year)
with open(infoname) as infile:
    for e, line in enumerate( infile.readlines() ):
        if e > 0:
            token = line.strip().split("\t")[0][1:].strip()
            value = line.strip().split("\t")[1].split()[-2]
            d[token] = float(value)/float(100)

dd = {}
for word in counter.keys():
    try:
        dd[word] = d[word] * counter[word]
    except:
        continue

import operator

sorted_x = sorted(dd.items(), key=operator.itemgetter(1))

print sorted_x
