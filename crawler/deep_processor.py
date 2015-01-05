#/usr/bin/python
from glob import glob
from newspaper import Article
import json

deeps = glob("./*-deep.json")
infos = glob("./backup/*.json")

deeps.sort()
infos.sort()

for deep, info in zip(deeps, infos):
    out_fname = deep.replace('deep','article')
    deep_j = json.loads(open(deep).read())
    info_j = json.loads(open(info).read())

    print deep, info, ":", len(deep_j), len(info_j)
    continue

    for i in deep_j:
        article = Article(i['url'])
        article.set_htmli['html']
        article.parse()

        text = a.text
