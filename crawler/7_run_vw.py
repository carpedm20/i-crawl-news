import os
import re
import subprocess
from glob import glob

def get_loss(output):
    pattern = 'average loss = (.*?)\n'
    m = re.search( pattern, output )
    loss = m.group(1)
    return float(loss[:-1])

losses = []
#no_zero

def get_cmd(testf, execute=False):
    trainf = testf.replace("test","train")
    modelf = testf.replace("test","model")
    predf = testf.replace("test","pred")
    outf = testf.replace("test","out")

    # vw-varinfo -c -b 24 --ngram 1 --passes 100 ./vw/GOOGL-1000-1000-2010-2014-train.vw
    #cmd = "vw -c %s --ngram 1 --passes 10000 --holdout_off -f %s 2>&1 | tee log.txt" % (trainf, modelf)
    a = open(trainf).readlines()
    #try:
    #    class_num = max([int(i.split('|')[0]) for i in a])
    #except:
    #    class_num = max([int(i.split('|')[0].split(' ')[0]) for i in a])
    #cmd = "vw -k -c --oaa %s %s --passes 20 --ngram 1 -f %s 2>&1 | tee log.txt" % (class_num+1, trainf, modelf)
    #cmd = "vw -k -c %s --passes 100 --holdout_off --ngram 1 -f %s 2>&1 | tee log.txt" % (trainf, modelf)
    cmd = "vw -k -c %s --passes 20  --ngram 1 -f %s 2>&1 | tee log.txt" % (trainf, modelf)
    print "==="
    print cmd
    if execute:
        os.system(cmd)
        with open('log.txt','r') as f:
            pass
            #losses.append([trainf, get_loss(f.read())])

    cmd = "vw %s -t -i %s -p %s" % (testf, modelf, predf)
    #print cmd

#for testf in glob("./mat/*-y-test.vw"):
#for testf in glob("./new/*-test.vw"):
for testf in glob("./wnew/*-test.evw"):
    get_cmd(testf, True)

#testf = "./vw/GOOGL-200-5000-2013-2014-tfidf-test.vw"
#get_cmd(testf)

from operator import itemgetter
losses = sorted(losses, key=itemgetter(1))
for i, j in losses:
    print i, j
