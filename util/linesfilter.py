#! /usr/bin/env python2.7
#coding=utf-8
#filename: filter.py
import sys
sys.path.append('../')
import os

def linesfilter(filename1, filename2):
    f1 = open(filename1)
    f2 = open(filename2)

    lines1 = f1.readlines()
    lines2 = f2.readlines()

    assert (len(lines1) == len(lines2))

    lines2write1 = []
    lines2write2 = []

    for i in xrange(len(lines1)):
        lines2write1.append(lines1[i])
        lines2write2.append(lines2[i])

    #filteredFilename1 = os.path.join(filename1, 'filtered')
    #filteredFilename2 = os.path.join(filename2, 'filtered')
    filteredFilename1 = filename1 + 'filtered'
    filteredFilename2 = filename2 + 'filtered'

    print 'ppp' , filename1
    print filteredFilename1

    f1 = open(filteredFilename1, 'w')
    f2 = open(filteredFilename2, 'w')
    f1.writelines(lines2write1)
    f2.writelines(lines2write2)
