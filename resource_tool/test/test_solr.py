# -*- coding: utf-8 -*-
import unittest
import urllib2
import solr_wrapper as sw


def getData(url):
    r = urllib2.urlopen(url)
    return eval(r.read())


class TestSolr(unittest.TestCase):

    def setUp(self):
        url1 = 'http://pine13.naist.jp:8983/solr/wikipedia/select?' \
               'q=title%3A%E5%A4%A7%E4%B9%85%E4%BF%9D%E5%88%A9%E9%80%9A' \
               '&wt=json&indent=true'
        self.res1 = getData(url1)['response']['docs']
        self.word1 = u'大久保利通'
        self.test1 = sw.search(self.word1).results
        url2 = 'http://pine13.naist.jp:8983/solr/wikipedia/select?' \
               'q=title%3A%E7%A6%8F%E6%B2%A2%E8%AB%AD%E5%90%89' \
               '&wt=json&indent=true'
        self.res2 = getData(url2)['response']['docs']
        self.word2 = u'福沢諭吉'
        self.test2 = sw.search(self.word2).results

    def test_search1(self):
        self.assertEqual(len(self.test1), len(self.res1))
        self.assertEqual(
            sorted([r['id'] for r in self.test1]),
            sorted([r['id'] for r in self.res1])
        )

    def test_search2(self):
        self.assertEqual(len(self.test2), len(self.res2))
        self.assertEqual(
            sorted([r['id'] for r in self.test2]),
            sorted([r['id'] for r in self.res2])
        )

    def test_getResponcefromTitle1(self):
        '''
        we except the document's id of 21011
        '''
        res = sw.getResponcefromTitle(self.word1)
        self.assertEqual(res['id'], '21011')

    def test_getResponcefromTitle2(self):
        '''
        we except the document's id of 8777
        '''
        res = sw.getResponcefromTitle(self.word2)
        self.assertEqual(res['id'], '8777')


if __name__ == '__main__':
    unittest.main()
