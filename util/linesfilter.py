#! /usr/bin/env python2.7
#coding=utf-8
#filename: filter.py
import sys
sys.path.append('../')
import os
import util.filter as Filter

def _getTextDicts(lineTexts):
    dicts = {}
    for line in lineTexts:
        temp = line.strip().split("\t")
        dicts[temp[0]] = temp[1]
    return dicts

def linesfilter(filename1, filename2):
    f1 = open(filename1)
    f2 = open(filename2)

    lines1 = f1.readlines()
    lines2 = f2.readlines()
    #can remove some lines which is too long..

    assert (len(lines1) == len(lines2))

    dicts1 = _getTextDicts(lines1)
    dicts2 = _getTextDicts(lines2)

    for text in dicts1.itervalues():
        print 'dict..', text


    lines2write1 = []
    lines2write2 = []

    for i in xrange(len(lines1)):
        templine1 = Filter.urlFilter(lines1[i])
        templine2 = Filter.urlFilter(lines2[i])
        templine1 = Filter.urlFilter(templine1)
        templine2 = Filter.urlFilter(templine2)
        lines2write1.append(templine1)
        lines2write2.append(templine2)

    filteredFilename1 = filename1 + '_filtered'
    filteredFilename2 = filename2 + '_filtered'

    print filteredFilename1

    f1 = open(filteredFilename1, 'w')
    f2 = open(filteredFilename2, 'w')
    f1.writelines(lines2write1)
    f2.writelines(lines2write2)
