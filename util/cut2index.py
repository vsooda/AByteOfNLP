#! /usr/bin/env python2.7
#coding=utf-8
#filename: cut2index.py
import sys
import jieba
sys.path.append('../')
import os

#generator new file which every word present with id
def cut2index(postFilename, commentFilename):
    fpost = open(postFilename)
    fcomment = open(commentFilename)
    postLines = fpost.readlines()
    commentLines = fcomment.readlines()
    #assert(len(postLines) == len(commentLines));
    #postLines = postLines.decode('utf-8')

    postLists = []
    for line in postLines:
        line = line.strip()
        seglist = jieba.cut(line)
        postLists.append(seglist)

    commentLists = []
    for line in commentLines:
        line = line.strip()
        seglist = jieba.cut(line)
        commentLists.append(seglist)

    print len(postLists)
    print len(commentLists)
    print ', '.join(postLists[0])

