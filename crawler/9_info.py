import os
import re
import subprocess
from glob import glob

#for trainf in glob("./new/*-x-train.vw"):
for trainf in glob("./wnew/AAPL*-x-train.evw"):
    #vw-varinfo -c --ngram 1 --passes 5000 --holdout_off ./vw/AAPL-250-4000-2010-2015-tfidf-train.vw
    varinfo = trainf.replace('train','varinfo')
    cmd = "vw-varinfo -c --passes 20 --ngram 1  %s > %s" % (trainf, varinfo)
    print cmd
    #if not os.path.isfile(varinfo):
    if True:
        os.system(cmd)
