#/usr/bin/python
import copy
import json
import timeit
from glob import glob
from multiprocessing import Pool

from newspaper import Article
from newspaper.outputformatters import OutputFormatter
from newspaper.cleaners import DocumentCleaner

def get_text(deep_i):
    url = deep_i['url']
    html = deep_i['html']

    article = Article(url, request_timeout=100)
    article.set_html(html)
    article.parse()
    text = article.text
    title = article.title

    return [url, [text, title]]

BACKUP_DIR = "backup"
DEEP_DIR = "deep_delay"

deeps = glob("./%s/*-deep.json" % DEEP_DIR)
deeps.sort()

pool = Pool(8)

for deep in deeps:
    out_fname = deep.replace('deep.','article.').replace(DEEP_DIR, "article")
    print out_fname
    info_fname = deep.replace('-deep.','.').replace(DEEP_DIR, BACKUP_DIR)

    try:
        deep_j = json.loads(open(deep).read())
    except:
        continue
    try:
        info_j = json.loads(open(info_fname).read())
    except:
        continue

    print "Pooling start"
    start = timeit.default_timer()
    texts = pool.map(get_text, deep_j)
    stop = timeit.default_timer()    
    print " => POOL : %s" % (stop - start)

    text_dict = dict(texts)

    for idx, deep_i in enumerate(deep_j):
        url = deep_i['url']
        html = deep_i['html']

        print "%s (%s/%s = %10.2f)" % (url, idx, len(deep_j), float(idx)/len(deep_j)*100.0)

        find = False
        for info_i in info_j:
            if info_i['href'] == url:
                info_i['text'] = text_dict[url][0]
                info_i['title'] = text_dict[url][1]
                find = True
            for sub in info_i['sub']:
                if sub['href'] == url:
                    sub['text'] = text_dict[url][0]
                    sub['title'] = text_dict[url][1]
                    find = True
                    break
            if find:
                break

        if not find:
            print "Error : %s" % url

    with open(out_fname, 'wb') as f:
        json.dump(info_j, f)
