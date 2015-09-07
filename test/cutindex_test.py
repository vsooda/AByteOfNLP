#! /usr/bin/env python2.7
#coding=utf-8
#filename: cut2index.py
import sys
import _init_paths
import os
from util.cut2index import *
from config import cfg

if __name__ == "__main__":
    stcpath = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH)
    postFile = os.path.join(stcpath, cfg.POST_FILENAME)
    commentFile = os.path.join(stcpath, cfg.COMMENT_FILENAME)
    postFileFiltered = postFile + cfg.FILTER_POSTFIX
    commentFileFiltered = commentFile + cfg.FILTER_POSTFIX
    print postFileFiltered

    cut2index(postFileFiltered, commentFileFiltered)


