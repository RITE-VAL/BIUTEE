# -*- coding: utf-8 -*-

import urllib2
from urllib import unquote_plus
from bs4 import BeautifulSoup

root = "http://ja.wikipedia.org"
items = [
    # "/wiki/%E3%82%AA%E3%82%B9%E3%83%9E%E3%83%B3%E5%B8%9D%E5%9B%BD"
    # "/wiki/%E3%83%A2%E3%83%B3%E3%82%B4%E3%83%AB%E5%B8%9D%E5%9B%BD"
    "/wiki/%E3%83%91%E3%83%95%E3%83%A9%E3%83%B4%E3%82%A3%E3%83%BC%E6%9C%9D"
]

while len(items) > 0:
    start = items.pop(0)
    response = urllib2.urlopen(root + start).read()
    soup = BeautifulSoup(response)
    main = soup.findAll('table', {"class": "infoboxCountryPrevSucc"})
    if len(main) == 0:
        continue
    assert(len(main) == 1)
    tds = list(main[0].tr.findAll('td'))
    if len(tds) == 0:
        continue
    assert(len(tds) == 3)
    print "{} {}".format(unquote_plus(start), tds[1])
    prev = tds[0]
    for a in [
        b for b in prev.findAll('a')
        if 'class' not in b.attrs and '/wiki' in b.attrs['href']
    ]:
        items.insert(0, a.attrs['href'].encode('utf-8'))
