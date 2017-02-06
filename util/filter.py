#! /usr/bin/env python2.7
#coding=utf-8
#filename: filter.py
import sys
sys.path.append('../')

import re

'''
convert the raw sentence to indexs
'''
url_pattern = re.compile("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+")
digit_pattern = re.compile('\d+\.?\d*')

def url_filter(contents):
    contents = re.sub(url_pattern, 'URL', contents)
    #print 'url filtering', contents
    return contents

def space_filter(contents):
    contents = re.sub('\s+', ' ', contents)
    return contents

def digit_filter(contents):
    contents = re.sub(digit_pattern, 'URL', contents)
    return contents

#remove the space which is not between two english word
def dirty_space_filter(contents):
    contents = contents


