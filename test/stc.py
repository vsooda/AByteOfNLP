#! /usr/bin/env python2.7
#coding=utf-8
#filename: stc.py
import sys
#sys.path.append('../')
import _init_paths
import jieba
from config import cfg
import os
from easydict import EasyDict as edict
from util.linesfilter import linesfilter
import util.filter as Filter

if __name__ == "__main__":
    print cfg.ROOT_DIR
    stcpath = os.path.join(cfg.ROOT_DIR, 'data/stc/')
    postFile = os.path.join(stcpath, 'repos/mini_post')
    commentFile = os.path.join(stcpath, 'repos/mini_comment')
    print stcpath
    print postFile
    print commentFile

    linesfilter(postFile, commentFile)
    print 'filer ok'

    #f = open(postFile, 'r')
    f = open(commentFile, 'r')
    lines = f.readlines()
    _data = edict()
    dicts = {}
    for line in lines:
        #temp = line.decode('utf-8').strip().split("\r")
        temp = line.strip().split("\t")
        dicts[temp[0]] = temp[1]

    #aa = dicts['repos-post-1000008610']
    aa = dicts['repos-cmnt-1000919120']
    print aa
    aa = Filter.urlFilter(aa)
    print aa
    segs = jieba.cut(aa)
    for w in segs:
        print w

