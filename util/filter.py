#! /usr/bin/env python2.7
#coding=utf-8
#filename: filter.py
import sys
sys.path.append('../')

import re

'''
convert the raw sentence to indexs
'''


def urlFilter(contents):
    urlpat = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
    contents = re.sub(urlpat, 'URL', contents)
    print 'url filtering', contents
    return contents



def spaceFiler(contents):
    contents = re.sub('\s+', ' ', contents)

def digitFilter(contents):
    digit = re.compile('\d+\.?\d*')
    contents = re.sub(urlpat, 'URL', contents)


