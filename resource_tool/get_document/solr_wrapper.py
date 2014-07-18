# -*- coding: utf-8 -*-
import solr

'''
 we must install solrpy
 > pip install solrpy
'''

url = 'http://pine13.naist.jp:8983/solr/wikipedia'
connection = solr.SolrConnection(url)


def search(word, tp=u'title'):
    if not isinstance(word, unicode):
        word = word.decode('utf-8')
    return connection.query(u'{}:{}'.format(tp, word))


def getResponcefromTitle(title):
    '''
    title で 検索する，万が一表記揺れが合った場合はリダイレクトをたどる
    '''
    if not isinstance(title, unicode):
        title = title.decode('utf-8')
    query = search(title, tp='title')
    results = [q for q in query.results if q['title'] == title]
    if len(results) == 0:
        return False
    elif '#REDIRECT' not in results[0][u'text']:
        return results[0]
    while '#REDIRECT' in results[0][u'text']:
        text = results[0][u'text']
        word = text.replace(u'#REDIRECT [[', '').replace(']]', '')
        query = search(word, tp='title')
        results = [q for q in query.results if q['title'] == word]
        if len(results) == 0:
            return False
    return results[0]


if __name__ == '__main__':
    pass
