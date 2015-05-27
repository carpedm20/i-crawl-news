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

for fname in glob("./mat/*-*.mat"):
    if '-250-4000-' not in fname:
        continue

    if 'interstellar' in fname:
        continue

    #outname = fname[:-4].replace("mat","wnew")
    outname = fname.replace('-250-4000-','-weight2-')
    dicname = fname.replace('-250-4000-','-prob-')+'-dic.pkl'

    #if os.path.isfile(outname):
    if False:
        print "%s already exists. continue..." % (outname)
        continue
    print "%s -> %s" % (fname, outname)

    dic = pickle.load(open(dicname))

    #Formats data for graph

    d = {}
    infoname = fname.replace('mat','wnew',1).replace('.mat','-tfidf-z-train.evw.info')
    print infoname
    with open(infoname) as infile:
        for e, line in enumerate( infile.readlines() ):
            if e > 0:
                token = line.strip().split("\t")[0][1:].strip()
                value = line.strip().split("\t")[1].split()[-2]
                d[token] = float(value)/float(100)
    infoname = fname.replace('mat','wnew',1).replace('.mat','-tfidf-z-test.evw.info')
    with open(infoname) as infile:
        for e, line in enumerate( infile.readlines() ):
            if e > 0:
                token = line.strip().split("\t")[0][1:].strip()
                value = line.strip().split("\t")[1].split()[-2]
                #value = line.strip().split("\t")[1].split(" ")[-1][:-1]
                d[token] = float(value)/float(100)

    weight = np.zeros((len(dic),1))

    error = 0
    for key, value in dic.items():
        try:
            weight[key] = d[value]
        except:
            error+=1
            pass
    print "%s : %s -> %s" % (len(dic), len(d), error)

    scipy.io.savemat(outname, mdict={'weight':weight})
    print " > %s complete" % (outname) 
