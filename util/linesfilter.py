#! /usr/bin/env python2.7
#coding=utf-8
#filename: filter.py
import sys
sys.path.append('../')
import os
import util.filter as Filter

#the key may be duplicate, so cann't use dict
def _getTextDicts(lineTexts):
    dicts = {}
    for line in lineTexts:
        temp = line.strip().split("\t")
        dicts[temp[0]] = temp[1]
    return dicts

def _getTextList(lineTexts):
    textlist = []
    for line in lineTexts:
        temp = line.strip().split("\t")
        textlist.append(temp[1])
    return textlist

#generator filter textfile
def linesfilter(postName, commentName, postfix):
    fpost = open(postName)
    fcomment = open(commentName)
    postLine = fpost.readlines()
    commentLine = fcomment.readlines()
    #can remove some lines which is too long..
    assert (len(postLine) == len(commentLine))
    postTextLines = _getTextList(postLine)
    commentTextLines = _getTextList(commentLine)
    postLineWrite = []
    commentLineWrite = []
    for i in xrange(len(postTextLines)):
        text = postTextLines[i]
        templine = Filter.urlFilter(text)
        templine = Filter.spaceFilter(templine)
        postLineWrite.append(templine + '\n')

    for i in xrange(len(commentTextLines)):
        text = commentTextLines[i]
        templine = Filter.urlFilter(text)
        templine = Filter.spaceFilter(templine)
        commentLineWrite.append(templine + '\n')

    filteredPostName = postName + postfix
    filteredCommentName = commentName + postfix
    print filteredPostName
    fpost = open(filteredPostName, 'w')
    fcomment = open(filteredCommentName, 'w')
    fpost.writelines(postLineWrite)
    fcomment.writelines(commentLineWrite)
