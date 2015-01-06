#/usr/bin/python
import copy
import json
import timeit
from glob import glob
from os.path import isfile
from multiprocessing import Pool

from newspaper import Article
from newspaper.outputformatters import OutputFormatter
from newspaper.cleaners import DocumentCleaner

BACKUP_DIR = "backup"
DEEP_DIR = "deep_delay"

def get_text(info):
    url = info[0]
    html = info[1]

    article = Article(url, request_timeout=100)
    article.set_html(html)
    article.parse()

    text = article.text
    title = article.title

    return [url, [text, title]]

TEST = True

pool = Pool(8)

companies = ['ibm','oracle','intel','google','apple','microsoft','facebook']
years = range(2010,2015)

for company in companies:
    for year in years:
        path = "./%s/%s-%s*-deep.json" % (DEEP_DIR, company, year)
        deeps = glob(path)
        
        for deep in deeps:
            out_fname = deep.replace('deep.','article.').replace(DEEP_DIR, "article")
            print out_fname
            info_fname = deep.replace('-deep.','.').replace(DEEP_DIR, BACKUP_DIR)

            if isfile(out_fname) and not TEST:
                print " ==> skip"
                continue

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
            params = [(deep_i['url'], deep_i['html']) for deep_i in deep_j]
            texts = pool.map(get_text, params)
            stop = timeit.default_timer()    
            print " => POOL : %s" % (stop - start)

            text_dict = dict(texts)

            for info_i in info_j:
                url = info_i['href']
                text = text_dict[url][0]
                title = text_dict[url][1]

                if text == '':
                    article = Article(url, request_timeout=100)
                    article.download()
                    article.parse()

                    text_dict[url][0] = article.text
                    text_dict[url][0] = article.title

                    if article.text == '':
                        print "Error %s" % url
                else:
                    info_i['text'] = text_dict[url][0]
                    info_i['title'] = text_dict[url][1]

            with open(out_fname, 'wb') as f:
                json.dump(info_j, f)
