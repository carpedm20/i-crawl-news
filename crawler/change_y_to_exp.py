import math
from glob import glob

for fname in glob("./wnew/inters*-train.vw"):
    with open(fname) as f:
        outfname = fname.replace(".vw",".evw")
        with open(outfname,'w') as outf:
            print "%s => %s" % (fname, outfname)
            for line in f.readlines():
                outf.write("%s %s" % (math.exp(-int(line.split(' ', 1)[0])), line.split(' ', 1)[1]))

for fname in glob("./wnew/inters*-test.vw"):
    with open(fname) as f:
        outfname = fname.replace(".vw",".evw")
        with open(outfname,'w') as outf:
            print "%s => %s" % (fname, outfname)
            for line in f.readlines():
                outf.write("%s %s" % (math.exp(-int(line.split(' ', 1)[0])), line.split(' ', 1)[1]))
