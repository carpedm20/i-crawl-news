#!/usr/bin/python
from glob import glob
from collections import Counter
from datetime import datetime, date, time
import json
import sys

is_cutoff = False

company = "google"
year = "2010"
month = "12"

dates = [range(19,23)]

d = datetime(year, 1, 1)

dates = ['Feb %s, 2010' % (month, d, year) for d in range(19,23)] \
        + ['Feb %s, 2010' % (month, d, year) for d in range(19,23)] \

articles = []
for ffname in glob("./bow/%s-%s-%s-bow.json" % (company, year, month)):
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
