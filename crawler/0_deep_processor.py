#/usr/bin/python
import copy
import json
import timeit
from glob import glob
from os.path import isfile
from multiprocessing import Pool, cpu_count

from newspaper import Article
from newspaper.outputformatters import OutputFormatter
from newspaper.cleaners import DocumentCleaner

import goose

BACKUP_DIR = "backup"
DEEP_DIR = "deep_delay"

g = goose.Goose()

def get_text_with_url(url):
    article = g.extract(url=url)
    text = article.cleaned_text
    title = article.title

    if text == '':
        article = Article(url, request_timeout=100)
        article.download()
        try:
            article.parse()
            text = article.text
            title = article.title
        except:
            text = ''

    return [text, title]

def get_text(info):
    url = info[0]
    html = info[1]

    try:
        article = Article(url, request_timeout=100)
        article.set_html(html)
        article.parse()

        text = article.text
        title = article.title

        if text == '':
            article = g.extract(raw_html = html)
            text = article.cleaned_text
            title = article.title
    except:
        try:
            article = g.extract(raw_html = html)
            text = article.cleaned_text
            title = article.title
        except:
            return [url, ['','']]

    return [url, [text, title]]

TEST = False

pool = Pool(cpu_count())

companies = ['google','apple','facebook','microsoft','ibm','oracle','intel']
years = range(2010,2015)

for company in companies:
    for year in years:
        path = "./%s/%s-%s*-deep.json" % (DEEP_DIR, company, year)
        deeps = glob(path)
        
        for deep in deeps:
            out_fname = deep.replace('deep.','article.').replace(DEEP_DIR, "article")
            info_fname = deep.replace('-deep.','.').replace(DEEP_DIR, BACKUP_DIR)
            print out_fname, info_fname

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
            #for idx,param in enumerate(params):
            #    print idx
            #    text = get_text(param)
            stop = timeit.default_timer()    
            print " => POOL : %s" % (stop - start)

            text_dict = dict(texts)

            for info_i in info_j:
                url = info_i['href']
                try:
                    text = text_dict[url][0]
                    title = text_dict[url][1]
                except:
                    text, title = get_text_with_url(url)

                if text == '' and title != '':
                    text, title = get_text_with_url(url)

                if text == '' and title != '':
                    info_j.remove(info_i)
                    print url
                else:
                    info_i['text'] = text
                    info_i['title'] = title

            if not TEST:
                with open(out_fname, 'wb') as f:
                    json.dump(info_j, f)
