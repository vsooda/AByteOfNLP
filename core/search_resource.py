#! /usr/bin/env python2.7
#coding=utf-8
#filename: search_resource.py

import core.textprocessing as tp

class ResourcesIndex :
    def __init__(self):
        self.resources = tp.get_csv_data('../data/resources.csv', 4)

    def dump(self):
        for index, res in self.resources.items():
            for k, v in res.items():
                print k, v
        print 'dump over'

#    def searchItem(self, keywords)

    #format: word: {"id", "weight"}
    def constructInvertIndex(self):
        self.invertIndex = {}
        for index, res in self.resources.items():
            for k, v in res.items():
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
