#/usr/bin/python
from glob import glob
from newspaper import Article
import json

BOW_DIR = "bow"

bows = glob("./%s/*-bow.json" % BOW_DIR)
bows.sort()

companies = ['google','apple','facebook', 'microsoft', 'ibm', 'oracle']
years = range(2010,2015)

word_count = {}
document_count = {}

for year in years:
    path = "./%s/*-%s-*-bow.json" % (BOW_DIR, year)

    word_count[year] = 0
    document_count[year] = 0

    for bow in glob(path):
        bow_j = json.loads(open(bow).read())

        for bow_i in bow_j:
            document_count[year] += 1
            word_count[year] += len(bow_i['words'].split())

    print "%s : %s %s => %10.4f" % (year,
           "{:,}".format(document_count[year]),
           "{:,}".format(word_count[year]),
           float(word_count[year])/document_count[year])

print "======================"

wc = 0
dc = 0

for year in years:
    wc += word_count[year]
    dc += document_count[year]

print "Total : %s %s => %10.4f" % ("{:,}".format(dc),
                                   "{:,}".format(wc),
                                   float(wc)/dc)
