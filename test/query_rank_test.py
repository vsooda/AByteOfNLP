#! /usr/bin/env python2.7
#coding=utf-8
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
#import _init_paths

from core import DictSentiment
import core.search_resource as sr
import core.synonyms as syno
import util.filter as Filter
import core.text_processing as tp


def test_space_filter(contents):
    filted = Filter.space_filter(contents)
    return filted


def test_filter():
    text = "sdfkjl sdkfj    sfj sdfj http://www.baidu.com "
    filted = test_space_filter(text)
    print filted

def print_result(scores, resources):
    print len(scores), ' results'
    #after sorted, the dict become a list
    scores = sorted(scores.iteritems(), key=lambda d:d[1], reverse=True)
    for score_item in scores:
        res_id = score_item[0]
        res_score = score_item[1]
        print "id: %d; name: %s; sent_type: %d; score: %.3f; keywords如下:" % (res_id, resources[res_id]['name'][0], resources[res_id]['sentiment_type'], res_score)
        otherKeywords = resources[res_id]['other']
        for word in otherKeywords:
            print '--- ', word

def test_query():
    ds = DictSentiment.DictSentiment()
    resources = tp.get_csv_data('../data/review/resources.csv', 4)
    resource_index = sr.ResourcesIndex(resources)
    resource_index.construct_invert_index_tfidf()
    resource_index.setup_sentenment_type(ds)
    #resource_index.dump()
    synos = syno.Synonyms()
    synos.construct_synoyms_index()

    while 1:
        query = raw_input('enter query: ')
        query = query.decode('utf8')
        sentiment_score = ds.single_sentiment_score(query)
        print "sent score: ", sentiment_score
        sent_type = ds.get_sentiment_type(sentiment_score)
        print sent_type
        words = []
        for sent in ds.sentences_words:
            words = words + sent
        output = ' '.join(words)
        print 'keywords: ', output
        expand_words = []
        for word in words:
            results = synos.query_synoyms(word)
            expand_words = expand_words + results
        expand_words = list(set(expand_words))

        output_expand = ' '.join(expand_words)
        print 'expand keywords: ', output_expand

        print '***********'
        scores = resource_index.search_item(words, sent_type)
        print_result(scores, resource_index.resources)
        print '***********'
        print '近义词扩展 result: '
        scores = resource_index.search_item(expand_words, sent_type)
        print_result(scores, resource_index.resources)
        print '***********'

if __name__ == "__main__":
    #test_filter()
    test_query()




