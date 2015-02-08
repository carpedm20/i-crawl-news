import numpy as np
import matplotlib.pyplot as plt

from __future__ import division

def finished():
    import subprocess
    subprocess.call(['python','/home/carpedm20/mail.py'])

%matplotlib inline
%load_ext autoreload
%autoreload 2

#######################
#
#######################

import time
import datetime
import scipy.io

start_year = 2014

start_date = datetime.datetime(start_year, 1, 1)
end_date = datetime.datetime(start_year, 12, 31)

mat = scipy.io.loadmat('GOOGL-%s.mat' % start_year)

R = mat.get('R')
maxes = mat.get('maxes')
data = mat.get('X')[0]
mat_dates = mat.get('date')[0]

dates = []
for date in mat_dates:
    dates.append(datetime.datetime.strptime(date[0], "%d-%b-%y").date())

#######################
#
#######################

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

plt.plot(dates,data)

#######################
#
#######################

import matplotlib.cm as cm
from pylab import *
from numpy import *

import matplotlib.dates as dt

fig = plt.figure(figsize=(18,16))

ax1 = fig.add_subplot(2,1,1)
ax1.plot(dates, data)
grid(True)

changes = []
run_length = []

pos = 0
for idx in xrange(1, len(maxes[:,0])-1):
    previous = maxes[idx-1][0]
    current = maxes[idx][0]
    
    if previous > current:
        ax1.plot(dates[idx-1],data[idx-1], 'ro')
        changes.append(idx-1)
        run_length.append(idx-1-pos)
        pos = idx-1
        
ax1.set_ylabel("Left Y-Axis Data")
ax1.set_xlabel("X-Axis Data")
ax1.set_title("Data Plotted on Left and Right Axis")

ax2 = fig.add_subplot(2, 1, 2)
sparsity = 3
ax2.pcolor(np.array(xrange(0, len(R[:,0]), sparsity)), 
          np.array(xrange(0, len(R[:,0]), sparsity)), 
          -np.log(R[0:-1:sparsity, 0:-1:sparsity]), 
          cmap=cm.Greys, vmin=0, vmax=1000)

ax2.set_xlabel('sample')
ax2.set_ylabel('cumulative sum')
ax2.set_title("Normal distrubution")

show()

#######################
#
#######################

from glob import glob
import json
import re
from nltk.corpus import stopwords
import math

from __future__ import division
stops = set(stopwords.words("english"))

from collections import Counter

files = glob('/home/carpedm20/git/i-crawl-news/crawler/bow/*.json')

file_reg =  '/home/carpedm20/git/i-crawl-news/crawler/bow/google-2014-*-bow.json'
files = glob(file_reg)

training_set = files

class Article(object):
    def __init__(self, idx, text, href, date):
        self.idx = idx
        self.text = text
        self.href = href
        self.date = date
        self.tfidf = None
        self.corpus = None

articles = []
article_dic = {}

count = 0
for f in training_set:
    print f
    j = json.loads(open(f).read())
    
    for article in j:
        try:
            date = datetime.datetime.strptime(article['date'], "%b %d, %Y").date()
        except:
            print "ERRR : %s" % article['date']
            continue
            
        text = article['text']
        
        article = Article(count, text, article['href'], date)
        
        articles.append(article)
        count += 1
        
        try:
            article_dic[date].append(article)
        except:
            article_dic[date] = []
            article_dic[date].append(article)

#######################
#
#######################

import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk import bigrams, trigrams
import math

from gensim import corpora, models, similarities

stopwords = nltk.corpus.stopwords.words('english')

print "Texts"
texts = [[word for word in document.text.lower().split() if word not in stopwords] for document in articles]

print "Remove texts"
#import itertools
#all_tokens = list(itertools.chain(*texts))
#tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
#texts = [[word for word in text if word not in tokens_once] for text in texts]

print "Dictionary"
dictionary = corpora.Dictionary(texts)
print "Corarticlespus"
corpus = [dictionary.doc2bow(t) for t in texts]

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

#lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=100)

print "Finished"

#######################
#
#######################

for idx, doc in enumerate(corpus_tfidf):
    articles[idx].tfidf = doc
    articles[idx].corpus = corpus[idx]

#######################
#
#######################

print changes, len(changes)
print run_length, len(run_length)

#######################
#
#######################

import gensim
def vec2dense(vec, num_terms):
    return gensim.matutils.corpus2dense([vec], num_terms=num_terms).T[0]

date_range = 10

vec_article_list = []
run_length_list = []

for idx, change in enumerate(changes):
    for gap in xrange(-date_range, date_range+1):
        new_date = dates[idx] + gap * datetime.timedelta(days=1)
        try:
            cur_articles = article_dic[new_date]
        except:
            continue

        for article in cur_articles:
            vec = vec2dense(article.corpus, len(dictionary))
            norm = sum(num for (tmp, num) in article.corpus)

            vec_article_list.append(vec/norm)
            run_length_list.append(run_length[idx])

#######################
#
#######################

nan_idx = []

for idx, article in enumerate(vec_article_list):
    if np.isnan(np.sum(article)):
        nan_idx.append(idx)
nan_idx.sort()
nan_idx.reverse()
for idx in nan_idx:
    del vec_article_list[idx]
    del run_length_list[idx]

#######################
#
#######################

import datetime

from sklearn.cross_validation import train_test_split
vec_article_train, vec_article_test, run_length_train, run_length_test = train_test_split(vec_article_list, run_length_list, test_size=0.33, random_state=42)

print len(vec_article_train), len(run_length_train)
print len(vec_article_test), len(run_length_test)

#######################
#
#######################

import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt

svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1e3)
svr_poly = SVR(kernel='poly', C=1e3, degree=2)

#clf = linear_model.SGDClassifier(n_jobs = -1)

%time clf = svr_rbf.fit(vec_article_train, run_length_train)

# http://stackoverflow.com/a/9300826/1676714
#from sklearn.cross_validation import ShuffleSplit
#cv = ShuffleSplit(3, test_fraction=0.2, train_fraction=0.2, random_state=0)
#gs = GridSeachCV(clf, params_grid, cv=cv, n_jobs=-1, verbose=2)
#%time gs.fit(articles_train, changes_train)

#y_rbf = svr_rbf.fit(articles_train, changes_train)
#y_lin = svr_lin.fit(X, y).predict(X)
#y_poly = svr_poly.fit(X, y).predict(X)

#######################
#
#######################

temp_length = 100

temp_test = vec_article_test[:temp_length]
temp_anwser = run_length_test[:temp_length]

%time temp_result = clf.predict(temp_test)

#######################
#
#######################

from sklearn.metrics import mean_squared_error
print " =======> %s" % mean_squared_error(temp_result, temp_anwser)

fig = plt.figure(figsize=(10,8))

ax1 = fig.add_subplot(1,1,1)
xs = range(len(temp_result))
ax1.scatter(xs, temp_result, c='b')
ax1.scatter(xs, temp_anwser, c='r')

print changes_train

finished()

#######################
#
#######################

print(__doc__)

import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt

###############################################################################
# Generate sample data
X = np.sort(5 * np.random.rand(40, 1), axis=0)
y = np.sin(X).ravel()

###############################################################################
# Add noise to targets
y[::5] += 3 * (0.5 - np.random.rand(8))

###############################################################################
# Fit regression model
svr_rbf = SVR(kernel='rbf', C=1e3, gamma=0.1)
svr_lin = SVR(kernel='linear', C=1e3)
svr_poly = SVR(kernel='poly', C=1e3, degree=2)
y_rbf = svr_rbf.fit(X, y).predict(X)
y_lin = svr_lin.fit(X, y).predict(X)
y_poly = svr_poly.fit(X, y).predict(X)

###############################################################################
# look at the results
plt.scatter(X, y, c='k', label='data')
plt.hold('on')
plt.plot(X, y_rbf, c='g', label='RBF model')
plt.plot(X, y_lin, c='r', label='Linear model')
plt.plot(X, y_poly, c='b', label='Polynomial model')
plt.xlabel('data')
plt.ylabel('target')
plt.title('Support Vector Regression')
plt.legend()
plt.show()
