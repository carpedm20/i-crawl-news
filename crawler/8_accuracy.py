import sys
import numpy as np
#from sklearn.metrics import accuracy_score as accuracy
from sklearn.metrics import mean_squared_error as accuracy
from sklearn.metrics import roc_auc_score as AUC
from sklearn.metrics import confusion_matrix

import os
import re
import subprocess
from glob import glob

losses = []

try:
    #for testf in glob("./vw/*-test.vw"):
    for testf in glob("./mat/*-y-test.vw"):
    #for testf in ['./vw/AAPL-250-4000-2014-2015-log-test.vw']:
        trainf = testf.replace("test","train")
        modelf = testf.replace("test","model")
        predf = testf.replace("test","pred")
        outf = testf.replace("test","out")

        cmd = "vw %s -t -i %s -p %s" % (testf, modelf, predf)
        print cmd
        if not os.path.isfile(predf):
            os.system(cmd)

        y_file = testf
        p_file = predf

        p = np.loadtxt( p_file )

        y_predicted = np.ones(( p.shape[0] ))

        y = np.loadtxt( y_file, usecols= [0] )
        max_y = max(y)

        losses.append([testf, accuracy( y, p), max_y])
except:
    pass

from operator import itemgetter
losses = sorted(losses, key=itemgetter(1))
for i, j, k in losses:
    print "%s\t%s\t%s" % (i, j, k)

print "====================================="
        
losses = sorted(losses, key=itemgetter(0))
for i, j, k in losses:
    print "%s\t%s\t%s" % (i, j, k)
        
