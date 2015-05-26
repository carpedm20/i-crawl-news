from __future__ import division

import gc
import os
import json
import time
import math
import pickle
import datetime
import scipy.io
import numpy as np
from glob import glob
from collections import Counter

from news_list import news_list

from sklearn.cross_validation import train_test_split

#start_y = 2014
#start_date = datetime.datetime(start_y, 1, 1)
#end_date = datetime.datetime(start_y, 12, 31)

company_dict = {'GOOGL':'google',
                'AAPL' :'apple',
                'FB'   :'facebook',
                'IBM'   :'ibm',
                'MSFT'   :'microsoft',
                'avengers' : 'the avengers movie',
                'frozen' : 'frozen movie',
                'inception' : 'inception movie',
                'knight' : 'the dark knight',
                'interstellar': 'interstellar movie',
                'JPY': 'yen',
                'KRW': 'korea won',
                'EUR': 'euro' }

#is_weighted = True
#is_cutoff = True
#is_weighted = False
#is_cutoff = False
is_weighted = False
is_date_weighted = True
is_cutoff = False
max_interval = 7
scale = 1000

import gensim
def vec2dense(vec, num_terms):
    return gensim.matutils.corpus2dense([vec], num_terms=num_terms).T[0]

import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams, trigrams
import math

from gensim import corpora, models, similarities

stopwords = nltk.corpus.stopwords.words('english')

class Article(object):
    def __init__(self, idx, text, href, date, related):
        self.idx = idx
        self.text = text
        self.href = href
        self.date = date
        self.related = related
        self.tfidf = None
        self.corpus = None

for fname in glob("./mat/*-*.mat"):
    if 'prob' in fname or 'weight' in fname or 'dic' in fname:
        continue

    outname = fname.replace('-250-4000-','-prob-')
    dicname = outname.replace('-prob-','-dic-')
    countname = outname.replace('-prob-','-count-')

    #if os.path.isfile(dicname):
    if False:
        print "%s already exists. continue..." % (dicname)
        continue

    print "%s -> %s" % (fname, outname)

    mat = scipy.io.loadmat(fname)

    split = fname[:-4].split('-')
    start_y, end_y = int(split[-2]), int(split[-1])

    company_sigil = fname.split('-')[0][6:]
    company = company_dict[company_sigil]

    R = mat.get('R')
    maxes = mat.get('maxes')
    try:
        data = mat.get('X')[0]
    except:
        print "ERROR : %s" % fname
        continue

    if type(mat.get('date')) == list:
        mat_dates = mat.get('date')[0]
    else:
        mat_dates = mat.get('date')

    if type(mat.get('date')) == np.ndarray and type(mat.get('date')[0]) != np.unicode_:
        mat_dates = mat_dates[0]

    dates = []
    for date in mat_dates:
        if type(date) == list:
            dd = date[0]
        elif type(date) == np.ndarray:
            dd = date[0]
        else:
            dd = date

        if dd == u'2010-01-':
            dd = u'2010-01-01'
        if dd == u'2011-01-':
            dd = u'2011-01-01'
        if dd == u'2012-01-':
            dd = u'2012-01-01'
        if dd == u'2013-01-0':
            dd = u'2013-01-01'
        if dd == u'2014-01-':
            dd = u'2014-01-01'

        try:
            dates.append(datetime.datetime.strptime(dd, "%d-%b-%y").date())
        except:
            try:
                dates.append(datetime.datetime.strptime(dd, "%Y-%m-%d").date())
            except:
                dates.append(datetime.datetime.strptime(dd, "%d-%b-%Y").date())

    bows = []
    for ffname in glob("./bow/%s-*-bow.json" % company):
        f_year = int(ffname.split("-")[1])

        if start_y <= f_year <= end_y:
            j = json.loads(open(ffname).read())
            bows.extend(j)

    count = 0
    articles = []
    article_dict = {}

    for bow in bows:
        if is_cutoff:
            if bow['name'] not in news_list:
                continue
        try:
            d = datetime.datetime.strptime(bow['date'], "%b %d, %Y").date()
        except:
            continue

        try:
            text = bow['words']
        except:
            continue
        if text != "":
            article = Article(count, text, bow['href'], d, bow['related'])
            articles.append(article)

            try:
                article_dict[d].append(article)
            except:
                article_dict[d] = []
                article_dict[d].append(article)
    del bows

    changes = []
    runs = []

    pos = 0
    for idx in xrange(1, len(maxes[:,0])-1):
        previous = maxes[idx-1][0]
        current = maxes[idx][0]

        if previous > current:
            changes.append(idx-1)
            runs.append(idx-1-pos)
            pos = idx-1

    print "%s~%s from %s. # of CP : %s" % (start_y,end_y, company, len(changes))
    print "Text processing start"

    texts = [[word for word in article.text.split()] for article in articles]

    dictionary = corpora.Dictionary(texts)
    with open(outname+'-dic.pkl','w') as f:
        pickle.dump(dictionary, f)

    corpus = [dictionary.doc2bow(t) for t in texts]
    del texts

    len_dictionary = len(dictionary)

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    print "Finished"

    for idx, doc in enumerate(corpus_tfidf):
        articles[idx].tfidf = doc
        articles[idx].corpus = corpus[idx]

    if not os.path.isfile(outname):

        vec_article_list = []
        run_length_list = []
        log_vec_article_list = []
        tfidf_vec_article_list = []

        hash_dict = {}
        run_dict = {}

        prob=np.ones((len(dictionary),150))

        for idx, change in enumerate(changes):
            date = dates[change]
            run = runs[idx]

            for gap in xrange(-run, 1):
                new_date = date + gap * datetime.timedelta(days=1)

                try:
                    cur_articles = article_dict[new_date]
                except:
                    continue

                for jdx, article in enumerate(cur_articles):
                    words = [i for (i,j) in article.corpus]

                    for word in words:
                        prob[word][-gap] += 1
                    #norm = sum(num for (tmp, num) in article.corpus)
                    #x = vec2dense(article.corpus, len_dictionary)/norm
                    #x = vec2dense(article.corpus, len_dictionary)

                    #hash_dict[hash(str(x))] = len(cur_articles)-jdx
                    #if article.related > 1:
                    #    hash_dict[hash(str(x))] = article.related
                    #else:
                    #    hash_dict[hash(str(x))] = 1
                    #run_dict[hash(str(x))] = run+gap

                    #vec_article_list.append(x)
                    #run_length_list.append(-gap)

        mat = scipy.io.savemat(outname,  mdict={'prob':prob})
        print " > %s complete" % outname

    if not os.path.isfile(countname):
        len_dictionary = len(dictionary)
        word_count = vec2dense(articles[0].corpus, len_dictionary)
        for article in articles[1:]:
            word_count += vec2dense(article.corpus, len_dictionary)
        mat = scipy.io.savemat(countname,  mdict={'word_count':word_count})
        print " > %s complete" % countname

    if not os.path.isfile(dicname):
        #articles = []
        #np.zeros((len(articles),len(dictionary)+1),dtype=np.int8)
        #count = 0
        new_articles = {}
        for k, v in article_dict.items():
            ddd = []
            for idx, i in enumerate(v):
                dd = []
                for corp in i.corpus:
                    #dd[corp[0]] = corp[1]
                    dd.append(corp[0])
                    #articles[count][corp[0]] = corp[1]
                ddd.append(dd)
                #count += 1
            new_articles[k.strftime("d%Y%m%d")]=np.array(ddd)

        scipy.io.savemat(dicname,  new_articles)
        print " > %s complete" % dicname
