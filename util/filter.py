#! /usr/bin/env python2.7
#coding=utf-8
#filename: filter.py
import sys
sys.path.append('../')

import re

'''
convert the raw sentence to indexs
'''
urlPattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
digitPattern = re.compile('\d+\.?\d*')

def urlFilter(contents):
    contents = re.sub(urlPattern, 'URL', contents)
    #print 'url filtering', contents
    return contents

def spaceFilter(contents):
    contents = re.sub('\s+', ' ', contents)
    return contents

def digitFilter(contents):
    contents = re.sub(digitPattern, 'URL', contents)
    return contents

#remove the space which is not between two english word
def dirtySpaceFilter(contents):
    contents = contents

