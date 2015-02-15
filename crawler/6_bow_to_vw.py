from __future__ import division

import gc
import os
import json
import time
import pickle
import datetime
import scipy.io
import numpy as np
from glob import glob

from sklearn.cross_validation import train_test_split

#start_y = 2014
#start_date = datetime.datetime(start_y, 1, 1)
#end_date = datetime.datetime(start_y, 12, 31)

is_weighted = True
company_dict = {'GOOGL':'google',
                'AAPL' :'apple',
                'FB'   :'facebook',
                'IBM'   :'ibm',
                'MSFT'   :'microsoft'}

is_weight = True
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

#lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)

#for fname in glob("./mat/*-%s-*.mat" % scale):
#for fname in glob("./mat/*-%s-*.mat" % scale):
for fname in glob("./mat/*-*.mat"):
    mat = scipy.io.loadmat(fname)
    outname = fname[:-4]

    if is_weighted:
        test_name = outname+'-tfidf-w-test.vw'
    else:
        test_name = outname+'-tfidf-x-test.vw'

    if os.path.isfile(test_name):
        print "%s already exists. continue..." % (outname+'-tfidf-test.vw')
        continue

    split = fname[:-4].split('-')
    start_y, end_y = int(split[-2]), int(split[-1])

    company_sigil = fname.split('-')[0][6:]
    company = company_dict[company_sigil]

    R = mat.get('R')
    maxes = mat.get('maxes')
    data = mat.get('X')[0]
    mat_dates = mat.get('date')[0]

    dates = []
    for date in mat_dates:
        dates.append(datetime.datetime.strptime(date[0], "%d-%b-%y").date())

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
        try:
            d = datetime.datetime.strptime(bow['date'], "%b %d, %Y").date()
        except:
            continue
        text = bow['words']
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

    vec_article_list = []
    run_length_list = []
    log_vec_article_list = []
    tfidf_vec_article_list = []

    hash_dict = {}

    print "Making list"
    for idx, change in enumerate(changes):
        date = dates[idx]
        run = runs[idx]

        #if run > max_interval:
        #    run = max_interval

        for gap in xrange(-run, 1):
            new_date = date + gap * datetime.timedelta(days=1)

            try:
                cur_articles = article_dict[new_date]
            except:
                continue

            for article in cur_articles:
                norm = sum(num for (tmp, num) in article.corpus)

                x = vec2dense(article.corpus, len_dictionary)/norm
                hash_dict[hash(str(x))] = article.related or 1

                vec_article_list.append(x)
                run_length_list.append(-gap)
    print "Finished making list"

    vec_article_train, vec_article_test, run_length_train, run_length_test = train_test_split(vec_article_list, run_length_list, test_size=0.33, random_state=42)
    del vec_article_list

    if is_weighted:
        trainf = outname+'-w-train.vw'
        testf = outname+'-w-test.vw'
    else:
        trainf = outname+'-x-train.vw'
        testf = outname+'-x-test.vw'

    with open(trainf,'w') as f:
        for vec, run in zip(vec_article_train, run_length_train):
            nonz = vec.nonzero()

            ans=" "
            for x, y in zip(nonz[0], vec[nonz]):
                ans += str(dictionary[x])+":"+str(y)+" "
                
            f.write(str(run+1) + " " + str(hash_dict[hash(str(vec))]) + " |" + ans[:-1] + "\n")

    with open(testf,'w') as f:
        for vec, run in zip(vec_article_test, run_length_test):
            nonz = vec.nonzero()

            ans=" "
            for x, y in zip(nonz[0], vec[nonz]):
                ans += str(dictionary[x])+":"+str(y)+" "
                
            f.write(str(run+1) + " " + str(hash_dict[hash(str(vec))]) + " |" + ans[:-1] + "\n")

    del vec_article_test, run_length_test, vec_article_train, run_length_train, hash_dict

    hash_dict = {}

    print "Making list"
    for idx, change in enumerate(changes):
        date = dates[idx]
        run = runs[idx]

        #if run > max_interval:
        #    run = max_interval

        for gap in xrange(-run, 1):
            new_date = date + gap * datetime.timedelta(days=1)

            try:
                cur_articles = article_dict[new_date]
            except:
                continue

            for article in cur_articles:
                x = np.log(1+vec2dense(article.corpus, len_dictionary))
                hash_dict[hash(str(x))] = article.related or 1

                log_vec_article_list.append(x)
    print "Finished making list"

    log_vec_article_train, log_vec_article_test, log_run_length_train, log_run_length_test = train_test_split(log_vec_article_list, run_length_list, test_size=0.33, random_state=42)
    del log_vec_article_list

    if is_weighted:
        trainf = outname+'-log-w-train.vw'
        testf = outname+'-log-w-test.vw'
    else:
        trainf = outname+'-log-x-train.vw'
        testf = outname+'-log-x-test.vw'

    with open(trainf,'w') as f:
        for vec, run in zip(log_vec_article_train, log_run_length_train):
            nonz = vec.nonzero()

            ans=" "
            for x, y in zip(nonz[0], vec[nonz]):
                ans += str(dictionary[x])+":"+str(y)+" "
                
            f.write(str(run+1) + " " + str(hash_dict[hash(str(vec))]) + " |" + ans[:-1] + "\n")

    with open(testf,'w') as f:
        for vec, run in zip(log_vec_article_test, log_run_length_test):
            nonz = vec.nonzero()

            ans=" "
            for x, y in zip(nonz[0], vec[nonz]):
                ans += str(dictionary[x])+":"+str(y)+" "
                
            f.write(str(run+1) +" " + str(hash_dict[hash(str(vec))]) + " |"+ ans[:-1] + "\n")

    del log_vec_article_train, log_run_length_train, log_vec_article_test, log_run_length_test, hash_dict

    hash_dict = {}

    print "Making list"
    for idx, change in enumerate(changes):
        date = dates[idx]
        run = runs[idx]

        #if run > max_interval:
        #    run = max_interval

        for gap in xrange(-run, 1):
            new_date = date + gap * datetime.timedelta(days=1)

            try:
                cur_articles = article_dict[new_date]
            except:
                continue

            for article in cur_articles:
                x = vec2dense(article.tfidf, len_dictionary)
                hash_dict[hash(str(x))] = article.related or 1

                tfidf_vec_article_list.append(x)
    print "Finished making list"

    tfidf_vec_article_train, tfidf_vec_article_test, tfidf_run_length_train, tfidf_run_length_test = train_test_split(tfidf_vec_article_list, run_length_list, test_size=0.33, random_state=42)
    del tfidf_vec_article_list
    del run_length_list

    if is_weighted:
        trainf = outname+'-tfidf-w-train.vw'
        testf = outname+'-tfidf-w-test.vw'
    else:
        trainf = outname+'-tfidf-x-train.vw'
        testf = outname+'-tfidf-x-test.vw'

    with open(trainf,'w') as f:
        for vec, run in zip(tfidf_vec_article_train, tfidf_run_length_train):
            nonz = vec.nonzero()

            ans=" "
            for x, y in zip(nonz[0], vec[nonz]):
                ans += str(dictionary[x])+":"+str(y)+" "
                
            f.write(str(run+1) + " " + str(hash_dict[hash(str(vec))]) + " |" + ans[:-1] + "\n")

    with open(testf,'w') as f:
        for vec, run in zip(tfidf_vec_article_test, tfidf_run_length_test):
            nonz = vec.nonzero()

            ans=" "
            for x, y in zip(nonz[0], vec[nonz]):
                ans += str(dictionary[x])+":"+str(y)+" "
                
            f.write(str(run+1) + " " + str(hash_dict[hash(str(vec))]) + " |"+ ans[:-1] + "\n")

    del tfidf_vec_article_train, tfidf_run_length_train, tfidf_vec_article_test, tfidf_run_length_test, hash_dict
    del dictionary
    del article_dict

    gc.collect()
