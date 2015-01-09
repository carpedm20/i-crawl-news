#/usr/bin/python
import requests

DATA_DIR = "data"
CSV_URL = 'http://www.google.com/finance/historical?q=%s&startdate=%s-01-01&enddate=%s-12-31&output=csv'

companies = ['ibm','oracle','intel','google','apple','microsoft','facebook']

symbols = {'ibm'       : 'IBM',
           'oracle'    : 'ORCL',
           'intel'     : 'INTC',
           'google'    : 'GOOGL',
           'apple'     : 'AAPL',
           'microsoft' : 'MSFT',
           'facebook'  : 'FB',
}
years = range(2010,2015)

for company in companies:
    print " [*] %s" % company
    url = CSV_URL % (symbols[company], 2010, 2015)

    with open('%s/%s.csv' % (DATA_DIR, company), 'wb') as f:
        r = requests.get(url, stream=True)

        if not r.ok:
            print "Error %s" % url
            continue
        for block in r.iter_content(1024):
            if not block:
                break

            f.write(block)
