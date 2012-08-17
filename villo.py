#!/usr/bin/python
# #-*- coding: utf-8 -*-
import urllib2
import json

from datetime import datetime
import time
import re

def timeit(method):

    def timed(*args, **kw):
        ts = time.time()
        result = method(*args, **kw)
        te = time.time()

        print '%r (%r, %r) %2.2f sec' %\
              (method.__name__, args, kw, te-ts)
        return result

    return timed

@timeit
def fetch_villo():
    url = 'http://api.citybik.es/villo.json'

    h = urllib2.urlopen(url)
    html = h.read()

    #fix JSON [see http://stackoverflow.com/a/4033740/410986 with a little modification in line 3]
    fixed_html = html
    fixed_html = re.sub(r"{\s*(\w)", r'{"\1', fixed_html)
    fixed_html = re.sub(r",\s*(\w)", r',"\1', fixed_html)
    fixed_html = re.sub(r"([a-z]):", r'\1":', fixed_html)

    data = json.loads(fixed_html)

    station = {}
    for d in data:
        station[d['name']]=d
    return station

if __name__ == '__main__':
    print '*'*80
    station = fetch_villo()
    target = ['louise','simonis','solbosch']

    print datetime.now()
    print '%40s - %5s - %5s'%('station','bikes','free')
    for t in target:
        for s in station.keys():
            if t in s.lower():
                print '%40s - %5s - %5s'%(s,station[s]['bikes'],station[s]['free'])

    print '*'*80