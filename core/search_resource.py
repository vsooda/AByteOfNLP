#! /usr/bin/env python2.7
#coding=utf-8
#filename: search_resource.py

import core.textprocessing as tp
import math

class ResourcesIndex :
    def __init__(self):
        self.resources = tp.get_csv_data('../data/resources.csv', 4)

    def constructDict(self):
        keywords =  []
        for index, res in self.resources.items():
            for k, words in res.items():
                #v = v.strip()
                #words = v.split(' ')
                keywords = keywords + words
        keywords = list(set(keywords))
        #writing to user dict
        pDict = open('../data/dict.tmp', 'wb+')
        firstline = True
        for k in keywords:
            if not firstline:
                pDict.write('\n')
            pDict.write(k)
            firstline = False
            print k
        pDict.close()


    def dump(self):
        for index, res in self.resources.items():
            for k, v in res.items():
                print k, v
        print 'dump over'


    #类型信息不该由这个关键词保存, 关键词只是纯粹的关键词序列
    def extractResourceKeywords(self):
        self.keywords = {}
        print 'keywords...'
        for index, res in self.resources.items():
            self.keywords[index] = [];
            for k, words in res.items():
                if k != 'type' and k != 'sentiment':
                    self.keywords[index] = self.keywords[index] + words
        for index, keywords in self.keywords.items():
            print index
            for word in keywords:
                print '... ', word

    def countTfidf(self):
        self.extractResourceKeywords()
        self.keywordWeight = {}
        for index, keywords in self.keywords.items():
            keyweights = {}
            #1.0 is wrong
            weight = 1.0 / len(keywords)
            for word in keywords:
                keyweights[word] = weight
            self.keywordWeight[index] = keyweights
        print self.keywordWeight
        #idf ok

        keyCounter = {}
        for index, keywords in self.keywords.items():
            for word in keywords:
                if word not in keyCounter:
                    keyCounter[word] = 0
                keyCounter[word] = keyCounter[word] + 1

        totalDocs = len(self.resources)
        print 'total doc num ', totalDocs

        for k, v in keyCounter.items():
            keyCounter[k] = math.log(totalDocs / v)
        print keyCounter

        for index, keywordWeights in self.keywordWeight.items():
            for word, weight in keywordWeights.items():
                idf = keyCounter[word]
                self.keywordWeight[index][word] = weight * idf

        print self.keywordWeight


    #format: word: {"id", "weight"}
    def constructInvertIndex(self):
        self.invertIndex = {}
        for index, res in self.resources.items():
            for k, words in res.items():
                for v in words:
                    if not v in self.invertIndex:
                        self.invertIndex[v] = []
                    item = {
                        "docid" : index,
                        "weight": 1.0
                    }
                    self.invertIndex[v].append(item)

    def constructInvertIndexTfidf(self):
        self.countTfidf()
        self.invertIndex = {}
        for index, keywords in self.keywords.items():
            for word in keywords:
                if not word in self.invertIndex:
                    self.invertIndex[word] = []
                item = {
                    "docid" : index,
                    "weight" : self.keywordWeight[index][word]
                }
                self.invertIndex[word].append(item)


    def invertIndexDump(self):
        for word, indexs in self.invertIndex.items():
            print word
            for index in indexs:
                print '...', index['docid'], index['weight']


    #input: keywords
    #output: top 5 resouces item name, and their weight
    def searchItem(self, keywords):
        scores = {}
        for k in keywords:
            #print 'searching ', k
            if k in self.invertIndex:
                #print 'invert key ', k
                items = self.invertIndex[k]
                for item in items:
                    docid = item['docid']
                    weight = item['weight']
                    if docid not in scores:
                        scores[docid] = 0
                    scores[docid] = scores[docid] + weight

        print len(scores), ' results'
        result = len(scores)
        if result <= 0:
            print 'no match'
            return
        #for docid, score in scores.items():
        #    print docid, self.resources[docid]['name'], score

        #after sorted, the dict become a list
        scores = sorted(scores.iteritems(), key=lambda d:d[1], reverse=True)
        for score in scores:
            print score[0], self.resources[score[0]]['name'][0], score[1]




