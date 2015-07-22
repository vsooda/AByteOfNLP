#! /usr/bin/env python2.7
#coding=utf-8
#filename: search_resource.py

import core.textprocessing as tp

class ResourcesIndex :
    def __init__(self):
        self.resources = tp.get_csv_data('../data/resources.csv', 4)

    def constructDict(self):
        keywords =  []
        for index, res in self.resources.items():
            for k, v in res.items():
                v = v.strip()
                words = v.split(' ')
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


    #need to do count weight and normalize
    #def countWeight

    #format: word: {"id", "weight"}
    def constructInvertIndex(self):
        self.invertIndex = {}
        for index, res in self.resources.items():
            for k, words in res.items():
                words = words.strip()
                word = words.split(' ')
                for v in word:
                    if not v in self.invertIndex:
                        self.invertIndex[v] = []
                    item = {
                        "docid" : index,
                        "weight": 1.0
                    }
                    self.invertIndex[v].append(item)


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
            print score[0], self.resources[score[0]]['name'], score[1]




