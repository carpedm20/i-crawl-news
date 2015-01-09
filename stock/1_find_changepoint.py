import numpy as np
import pandas as pd

from __future__ import division

DATA_DIR = './data'

companies = ['ibm','oracle','intel','google','apple','microsoft','facebook']

symbols = {'ibm'       : 'IBM',
           'oracle'    : 'ORCL',
           'intel'     : 'INTC',
           'google'    : 'GOOGL',
           'apple'     : 'AAPL',
           'microsoft' : 'MSFT',
           'facebook'  : 'FB',
}

for company in companies:
    df = pd.io.parsers.read_csv('%s/%s.csv' % (DATA_DIR, company))

    r_df = df.reindex(index=df.index[::-1])
    data = r_df['Open'].values

    q, P, Pcp = offcd.offline_changepoint_detection(data, partial(offcd.const_prior, l=(len(data)+1)), offcd.gaussian_obs_log_likelihood, truncate=-20)
