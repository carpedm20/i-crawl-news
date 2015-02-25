import sys
import numpy as np
#from sklearn.metrics import accuracy_score as accuracy
from sklearn.metrics import mean_squared_error as accuracy
from math import sqrt

from sklearn.metrics import roc_auc_score as AUC
from sklearn.metrics import confusion_matrix

import os
import re
import subprocess
from glob import glob

losses = []
error_dict = {}

#accuracy_check_mode = True # with numpy
accuracy_check_mode = False# with numpy
#accuracy_check_mode = False # with numpy

#try:
if True:
    #for testf in glob("./mat/*-w-test.vw"):
    #for testf in glob("./mat/*-y-test.vw"):
    #for testf in glob("./new/AAPL*-2010-2015-log-x-test.vw"):
    #for testf in glob("./wnew/*-2010-2015-log-z-test.vw"):
    #for testf in glob("./wnew/AAPL*-log-x-test.vw"):
    #for testf in glob("./wnew/*2010-2015*-x-test.evw"):
    for testf in glob("./wnew/*-test.evw"):
    #for testf in glob("./wnew/*-z-test.vw"):
    #for testf in ["./vw/AAPL-250-4000-2011-2012-test.vw",
    #              "./mat/AAPL-250-4000-2011-2012-y-test.vw"]:
    #for testf in glob("./mat/*-y-test.vw"):
    #for testf in ['./vw/AAPL-250-4000-2014-2015-log-test.vw']:
        trainf = testf.replace("test","train")
        modelf = testf.replace("test","model")
        predf = testf.replace("test","pred")
        outf = testf.replace("test","out")
        rawf = testf.replace("test","raw")

        cmd = "vw %s -t -i %s -p %s -r %s" % (testf, modelf, predf, rawf)
        print cmd
        #if not os.path.isfile(predf):
        if not accuracy_check_mode:
            os.system(cmd)

        y_file = testf
        p_file = predf

        p = np.loadtxt(p_file, usecols=[0])
        y = np.loadtxt(y_file, usecols=[0])
        max_y = max(y)

        if accuracy_check_mode:
            lines = open(trainf).readlines()
            #q = [-int(l.split(" '", 1)[1].split(" ", 1)[0]) for l in lines]
            #for (i, j) in zip(y, y-p):
            for (i, j) in zip(y, p):
                #print i, j
                losses.append([i, j])
        else:
            losses.append([testf, sqrt(accuracy( y, p)), max_y])
            #losses.append([testf, (accuracy( y, p)), max_y])

#except:
#    pass

if len(losses[0]) == 2:
    #for i in losses:
    #    print i
    print "just pass"
    pass
else:
    from operator import itemgetter
    losses = sorted(losses, key=itemgetter(1))
    for i, j, k in losses:
        print "%s  %.4f  %s" % (i, j, k)

    print "====================================="
            
    ll = []
    losses = sorted(losses, key=itemgetter(0))
    for com in ['AAPL','FB','GOOGL','IBM','MSFT']:
        for ex in ['log','tfidf']:
            target = "\n%s,%s" % (com,ex)
            if target not in ll:
                print target
                ll.append(target)
            avg = 0
            if ex == 'log':
                print "& LOG1P+  ",
            else:
                print "& TFIDF+  ",
            if com == 'FB':
                print "&   ",
                for year in ['2011-2012','2012-2013','2013-2014','2014-2015','2011-2015']:
                    for i, j, k in losses:
                        if com in i and ex in i and year in i:
                            #print "%s  %.4f  %s" % (i, j, k)
                            print "& %.4f  " % j,
                            avg += float(j)
                print "& %.4f   \\\\" % (avg/5),
            else:
                for year in ['2010-2011','2011-2012','2012-2013','2013-2014','2014-2015','2010-2015']:
                    for i, j, k in losses:
                        if com in i and ex in i and year in i:
                            #print "%s  %.4f  %s" % (i, j, k)
                            print "& %.4f  " % j,
                            avg += float(j)
                print "& %.4f   \\\\" % (avg/6),
        avg = 0
        target = "\n%s,x" % (com)
        if target not in ll:
            print target
            ll.append(target)
        print "& TF+  ",
        if com == 'FB':
            print "&   ",
            for year in ['2011-2012','2012-2013','2013-2014','2014-2015','2011-2015']:
                for i, j, k in losses:
                    if com in i and 'log' not in i and 'tfidf' not in i and year in i:
                        #print "%s  %.4f  %s" % (i, j, k)
                        print "& %.4f  " % j,
                        avg += float(j)
            print "& %.4f   \\\\" % (avg/6),
        else:
            for year in ['2010-2011','2011-2012','2012-2013','2013-2014','2014-2015','2010-2015']:
                for i, j, k in losses:
                    if com in i and 'log' not in i and 'tfidf' not in i and year in i:
                        #print "%s  %.4f  %s" % (i, j, k)
                        print "& %.4f  " % j,
                        avg += float(j)
            print "& %.4f \\\\" % (avg/6),
