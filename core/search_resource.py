#! /usr/bin/env python2.7
#coding=utf-8
#filename: search_resource.py

import core.textprocessing as tp

class ResourcesIndex :
    def __init__(self):
        self.resources = tp.get_csv_data('../data/resources.csv', 4)

    def dump(self):
        for res in self.resources:
            for k, v in res.items():
                print k, v
        print 'dump over'
