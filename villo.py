#!/usr/bin/python
# #-*- coding: utf-8 -*-
import urllib2
from datetime import datetime
import time

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

    station = {}
    for station_str in html[1:-1].split('{'):
        if station_str is not '':
            data = {}
            fields_str = station_str.split('}')[0].split(',')
            for f in fields_str:
                kv = f.split(':')
                if kv[0] == ' timestamp':
                    key = 'timestamp'
                    value = ':'.join(kv[1:])
                else:
                    key = kv[0].strip()
                    value = kv[1]
                value = value.replace('"','')
                data[key]=value
            station[data['name']]=data
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