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

company_dict = {'GOOGL':'google',
                'AAPL' :'apple',
                'FB'   :'facebook'}

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
    def __init__(self, idx, text, href, date):
        self.idx = idx
        self.text = text
        self.href = href
        self.date = date
        self.tfidf = None
        self.corpus = None

#lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)

#for fname in glob("./mat/*-%s-*.mat" % scale):
for fname in glob("./mat/*-%s-*.mat" % scale):
    mat = scipy.io.loadmat(fname)
    outname = fname[:-4]

    if os.path.isfile(outname+'-tfidf-test.vw'):
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
            article = Article(count, text, bow['href'], d)
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
    len_dictionary = len(dictionary)
    del dictionary

    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]

    print "Finished"

    for idx, doc in enumerate(corpus_tfidf):
        articles[idx].tfidf = doc
        articles[idx].corpus = corpus[idx]

    vec_article_list = []
    run_length_list = []
    tfidf_vec_article_list = []
    tfidf_run_length_list = []

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

                vec_article_list.append(vec2dense(article.corpus, len_dictionary)/norm)
                run_length_list.append(-gap)

                tfidf_vec_article_list.append(vec2dense(article.tfidf, len_dictionary))
                tfidf_run_length_list.append(-gap)

    """
    nan_idx = []

    for idx, article in enumerate(vec_article_list):
        if np.isnan(np.sum(article)):
            nan_idx.append(idx)
    nan_idx.sort()
    nan_idx.reverse()
    for idx in nan_idx:
        del vec_article_list[idx]
        del run_length_list[idx]
    """

    vec_article_train, vec_article_test, run_length_train, run_length_test = train_test_split(vec_article_list, run_length_list, test_size=0.33, random_state=42)
    tfidf_vec_article_train, tfidf_vec_article_test, tfidf_run_length_train, tfidf_run_length_test = train_test_split(tfidf_vec_article_list, tfidf_run_length_list, test_size=0.33, random_state=42)

    with open(outname+'-train.vw','w') as f:
        for vec, run in zip(vec_article_train, run_length_train):
            nonz = vec.nonzero()

            ans=" "
            for x, y in zip(nonz[0], vec[nonz]):
                ans += str(x)+":"+str(y)+" "
                
            f.write(str(run+1) + ans[:-1] + "\n")

    with open(outname+'-test.vw','w') as f:
        for vec, run in zip(vec_article_test, run_length_test):
            nonz = vec.nonzero()

            ans=" "
            for x, y in zip(nonz[0], vec[nonz]):
                ans += str(x)+":"+str(y)+" "
                
            f.write(str(run+1) +" |"+ ans[:-1] + "\n")

    with open(outname+'-tfidf-train.vw','w') as f:
        for vec, run in zip(tfidf_vec_article_train, tfidf_run_length_train):
            nonz = vec.nonzero()

            ans=" "
            for x, y in zip(nonz[0], vec[nonz]):
                ans += str(x)+":"+str(y)+" "
                
            f.write(str(run+1) + ans[:-1] + "\n")

    with open(outname+'-tfidf-test.vw','w') as f:
        for vec, run in zip(tfidf_vec_article_test, tfidf_run_length_test):
            nonz = vec.nonzero()

            ans=" "
            for x, y in zip(nonz[0], vec[nonz]):
                ans += str(x)+":"+str(y)+" "
                
            f.write(str(run+1) +" |"+ ans[:-1] + "\n")

    print "%s. max run : %s" % (outname, max(run_length_list))
    gc.collect()
