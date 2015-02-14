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
    for testf in glob("./vw/*2010-*-test.vw"):
        trainf = testf.replace("test","train")
        modelf = testf.replace("test","model")
        predf = testf.replace("test","pred")
        outf = testf.replace("test","out")

        if not os.path.isfile(predf):
            cmd = "vw %s -t -i %s -p %s" % (testf, modelf, predf)
            os.system(cmd)

        y_file = testf
        p_file = predf

        p = np.loadtxt( p_file )

        y_predicted = np.ones(( p.shape[0] ))

        y = np.loadtxt( y_file, usecols= [0] )
        max_y = max(y)

        losses.append([testf, accuracy( y, y_predicted ), max_y])
except:
    pass

from operator import itemgetter
losses = sorted(losses, key=itemgetter(1))
for i, j, k in losses:
    print i, j, k
        
