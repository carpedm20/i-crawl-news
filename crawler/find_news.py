from glob import glob
import json

is_cutoff = False
company = "apple"
word = "newsletters"

bows = []

for ffname in glob("./bow/%s-*bow.json" % company):
    print ffname,
    f_year = int(ffname.split("-")[1])

    j = json.loads(open(ffname).read())
    bows.extend(j)

count = 0
articles = []
article_dict = {}

for bow in bows:
    if is_cutoff:
        if bow['name'] not in news_list:
            continue
    text = bow['words']

    if word in text:
        articles.append(bow)
        print text

