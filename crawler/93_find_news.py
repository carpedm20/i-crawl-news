#!/usr/bin/python
from glob import glob
from collections import Counter
from datetime import datetime, date, time, timedelta
import json
import sys
from collections import OrderedDict
from utils import company_dict
import nltk.data
import re
from nltk.corpus import stopwords

tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

company_dict = dict((v, k) for k, v in company_dict.items())

is_cutoff = False

#month = 12

company = "google"
year = 2013
dates = range(19,23) + range(1,10)
dates_idx = [4, 5, 8, 9, 11, 12] # bad
dates_idx = [43, 48, 49] # good
#dates_idx = [57, 58, 59] # good
#dates_idx = range(17,32)  # good
dates_idx = range(92,97)  # good

#company = "apple"
#year = 2014
#dates_idx = [28, 109] # good
#dates_idx = range(8, 14) # good
#dates_idx = range(25,26) # good
#dates_idx = range(70, 75) # good

start_date = datetime(year, 1, 1)
day1 =  timedelta(days=1)
dates = [start_date + (date-1) * day1 for date in dates_idx]
dates = [date.strftime("%b %d, %Y").replace(' 0',' ') for date in dates]
dates = ["May %d, 2013" % date for date in range(14,22)]

#print dates

articles = {}
for date in dates:
    articles[date] = []

for ffname in glob("./bow/%s-%s-*-bow.json" % (company, year)):
    f_year = int(ffname.split("-")[1])
    j = json.loads(open(ffname).read())

    for i in j:
        if i['date'] in dates:
            articles[i['date']].append(i)

infoname = "./wnew/%s-250-4000-%s-%s-tfidf-z-train.evw.info" % (company_dict[company], year, year)

word_d = {}
with open(infoname) as infile:
    for e, line in enumerate( infile.readlines() ):
        if e > 0:
            token = line.strip().split("\t")[0][1:].strip()
            value = line.strip().split("\t")[1].split()[-2]
            word_d[token] = float(value)/float(100)
            #word_d[token] = abs(float(value))

date_score_sentences = {}
for date, articles in articles.items():
    """print "================================================"
    print date
    print "================================================"

    for article in articles:
        print "------------------------------------------------"
        print article['title']
        print "------------------------------------------------"
        print article['text']"""

    score_sentences = {}
    for article in articles:
        for sentence in tokenizer.tokenize(article['text']):
            score = 0

            letters_only = re.sub("[^a-zA-Z]", " ", sentence)
            words = letters_only.lower().split()
            stops = set(stopwords.words("english"))

            meaningful_words = [w for w in words if not w in stops]

            for w in meaningful_words:
                try:
                    score += word_d[w]
                except:
                    continue
            try:
                #score_sentences[sentence] = [score/len(meaningful_words), article['href']]
                score_sentences[sentence] = [score, article['href']]
            except:
                pass

    d = OrderedDict(sorted(score_sentences.items(), key=lambda t: t[1]))
    date_score_sentences[''] = d

def sentence_info(score, sentence, word_d, latex_mode=True):
    letters_only = re.sub("[^a-zA-Z]", " ", sentence)
    words = letters_only.lower().split()
    stops = set(stopwords.words("english"))

    meaningful_words = [w for w in words if not w in stops]
    d = {}
    for w in meaningful_words:
        try:
            d[w] = word_d[w]
        except:
            pass
    d = OrderedDict(sorted(d.items(), key=lambda t: t[1]))
    if latex_mode:
        for word in sentence.split():
            #if re.sub("[^a-zA-Z]", "", word).lower() in d.keys()[-5:]:
            if re.sub("[^a-zA-Z]", "", word).lower() in d.keys()[len(d)/2:len(d)/2+6]:
            #if re.sub("[^a-zA-Z]", "", word).lower() in d.keys()[:5]:
                sentence = sentence.replace(word, "\\textbf{%s}" % word)
    print score, sentence
    for a, b in d.items():
        print "=", a, b

#d = OrderedDict(sorted(score_sentences.items(), key=lambda t: t[1]))
for (date, d), d_idx in zip(date_score_sentences.items(), dates_idx):
    print "================================================"
    print "================================================"
    print date, "(", d_idx, ")"
    print "================================================"
    print "================================================"
    print "length :", len(d.items())

    for a, b in d.items()[-16:]:
    #for a, b in d.items()[:5]:
        print "----------------------------------------------------------------"
        sentence_info(b, a, word_d)
    """print "##############################################################"
    print "##############################################################"
    for a, b in d.items()[:6]:
        print b, a
        sentence_info(a, word_d)
        print "----------------------------------------------------------------"
    """
    raw_input()


"""
dates = [a['date'] for a in articles]
dates.sort()
dates = list(set(dates))

 + datetime.timedelta(days=1)

for date in dates:
    words = []
    for a in articles:
        if a['date'] == date:
            words.extend(a['words'].split())
"""
