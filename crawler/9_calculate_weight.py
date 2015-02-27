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
    if 'prob' in fname:
        continue

    outname = fname[:-4].replace("mat","wnew")
    dicname = fname.replace('-250-4000-','-prob-')+'-dic.pkl'

    if os.path.isfile(outname):
        print "%s already exists. continue..." % (outname)
        continue
    print "%s -> %s" % (fname, outname)

    dic = pickle.load(open(dicname))

    #Formats data for graph

    with open("wnew/AAPL-250-4000-2010-2010-log-z-train.evw.info") as infile:
        d = {}
        for e, line in enumerate( infile.readlines() ):
            if e > 0:
                token = line.strip().split("\t")[0][1:].strip()
                value = line.strip().split("\t")[1].split()[-2]
                d[token] = float(value)/float(100)


    for word in dic:

