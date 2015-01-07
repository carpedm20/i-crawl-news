#/usr/bin/python
from glob import glob
from newspaper import Article
import progressbar
import json

BACKUP_DIR = "backup"
DEEP_DIR = "deep_delay"

deeps = glob("./%s/*-deep.json" % DEEP_DIR)
deeps.sort()

for deep in deeps:
    info = deep.replace('-deep.','.').replace(DEEP_DIR, BACKUP_DIR)

    try:
        info_j = json.loads(open(info).read())
        count = len(info_j)
        for info_i in info_j:
            count += len(info_i['sub'])

        #print info, ":", count

    except:
        continue

    try:
        deep_j = json.loads(open(deep).read())
        #print deep, ":", len(deep_j)
    except:
        continue

    urls = [info['href'] for info in info_j]
    subs = [sub['href'] for sub in info['sub'] for info in info_j]

    urls += subs

    deep_urls = [deep_i['url'] for deep_i in deep_j]

    print deep, count, ">=", len(deep_j), ':', count >= len(deep_j), ":", len(list(set(urls) - set(deep_urls)))

