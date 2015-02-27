syear='2010'
eyear='2014'
#feature='-tfidf'
feature=''
addition='x'

fname = './wnew/AAPL-250-4000-%s-%s%s-%s-train.evw.info' % (syear, eyear, feature, addition)
with open(fname) as f:
    print fname
    lines = f.readlines()
    for line in lines[1:9]:
        print "%s %s" % (line.split()[0][1:], line.split()[-2])
    for line in lines[-8:]:
        print "%s %s" % (line.split()[0][1:], line.split()[-2])
