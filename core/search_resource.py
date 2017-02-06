#! /usr/bin/env python2.7
#coding=utf-8
#filename: search_resource.py

import math

class ResourcesIndex :
    def __init__(self, resources):
        self.resources = resources

    def construct_dict(self):
        keywords =  []
        for index, res in self.resources.items():
            for k, words in res.items():
                #v = v.strip()
                #words = v.split(' ')
                keywords = keywords + words
        keywords = list(set(keywords))
        #writing to user dict
        pDict = open('../data/review/dict.tmp', 'wb+')
        firstline = True
        for k in keywords:
            if not firstline:
                pDict.write('\n')
            pDict.write(k)
            firstline = False
            #print k
        pDict.close()

    def setup_sentenment_type(self, ds):
        for index, res in self.resources.items():
            sentiment = res["sentiment"]
            sentiment_score = ds.get_single_sent_count(sentiment)
            sent_type = ds.get_sentiment_type(sentiment_score)
            #print "sent score: ", sentiment_score, sent_type
            res['sentiment_type'] = sent_type


    def dump(self):
        for index, res in self.resources.items():
            for k, v in res.items():
                if k != 'sentiment_type':
                    print k, ' '.join(v)
                else:
                    print k, v
        print 'dump over'


    #类型信息不该由这个关键词保存, 关键词只是纯粹的关键词序列
    def extract_resource_keywords(self):
        self.keywords = {}
        print 'keywords...'
        for index, res in self.resources.items():
            self.keywords[index] = [];
            for k, words in res.items():
                if k != 'type' and k != 'sentiment':
                    self.keywords[index] = self.keywords[index] + words

    def count_tfidf(self):
        self.extract_resource_keywords()
        self.keywordWeight = {}
        for index, keywords in self.keywords.items():
            keyweights = {}
            keysets = list(set(keywords))
            for word in keysets:
                occurTime = keywords.count(word)
                weight = occurTime * 1.0 / len(keywords)
                keyweights[word] = weight
                #print index, word, occurTime, len(keywords), weight
            self.keywordWeight[index] = keyweights
            self.keywords[index] = keysets
        #print self.keywordWeight
        #idf ok

        #去重
        #for index, keywords in self.keywords.items():
        #    print index
        #    for word in keywords:
        #        print '... ', word

        keyCounter = {}
        for index, keywords in self.keywords.items():
            for word in keywords:
                if word not in keyCounter:
                    keyCounter[word] = 0
                keyCounter[word] = keyCounter[word] + 1

        totalDocs = len(self.resources)
        print 'total doc num ', totalDocs

        for k, v in keyCounter.items():
            idfWeight = math.log(totalDocs / v)
            keyCounter[k] = idfWeight
            #print k, v, totalDocs, idfWeight
        #print keyCounter

        for index, keywordWeights in self.keywordWeight.items():
            for word, weight in keywordWeights.items():
                idf = keyCounter[word]
                self.keywordWeight[index][word] = weight * idf

        #print self.keywordWeight


    #format: word: {"id", "weight"}
    def construct_invert_index(self):
        self.invert_index = {}
        for index, res in self.resources.items():
            for k, words in res.items():
                for v in words:
                    if not v in self.invert_index:
                        self.invert_index[v] = []
                    item = {
                        "docid" : index,
                        "weight": 1.0
                    }
                    self.invert_index[v].append(item)

    def construct_invert_index_tfidf(self):
        self.count_tfidf()
        self.invert_index = {}
        for index, keywords in self.keywords.items():
            for word in keywords:
                if not word in self.invert_index:
                    self.invert_index[word] = []
                item = {
                    "docid" : index,
                    "weight" : self.keywordWeight[index][word]
                }
                self.invert_index[word].append(item)


    def invert_index_dump(self):
        for word, indexs in self.invert_index.items():
            print word
            for index in indexs:
                print '...', index['docid'], index['weight']


    #input: keywords
    #output: top 5 resouces item name, and their weight
    def search_item(self, keywords, sentiment_type=0):
        scores = {}
        for k in keywords:
            if k in self.invert_index:
                items = self.invert_index[k]
                for item in items:
                    docid = item['docid']
                    weight = item['weight']
                    if docid not in scores:
                        scores[docid] = 0
                    scores[docid] = scores[docid] + weight
                    #print weight
        if sentiment_type != 0:
            for docid, score in scores.items():
                doc_sent_type = self.resources[docid]['sentiment_type']
                if doc_sent_type * sentiment_type < 0:
                    scores[docid] = scores[docid] - 1
                elif doc_sent_type == sentiment_type:
                    scores[docid] = scores[docid] + 0.2

        return scores


