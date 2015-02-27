from collections import Counter
from glob import glob
import json

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
    if i[1] > 200:
        print "'%s'," % i[0]
