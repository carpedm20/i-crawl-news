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

for testf in glob("./vw/*-test.vw"):
    trainf = testf.replace("test","train")
    modelf = testf.replace("test","model")
    predf = testf.replace("test","pred")
    outf = testf.replace("test","out")
    rawf = testf.replace("test","raw")

    cmd = "vw %s -t -i %s -p %s -r %s" % (testf, modelf, predf, rawf)

