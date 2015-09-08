#! /usr/bin/env python2.7
#coding=utf-8
#filename: cut2index.py
from __future__ import absolute_import
import sys
import _init_paths
import os
from util.cut2index import *
from config import cfg
from keras.preprocessing.sequence import pad_sequences
import numpy as np
from  keras_theano.seq2seq import seq2seq, batchSeq2seq

def to_one_hot(id):
    zeros = [0] * maxFeatures
    zeros[id] = 1
    return zeros

if __name__ == "__main__":
    #pickle_test()
    stcpath = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH)
    postFile = os.path.join(stcpath, cfg.POST_FILENAME)
    commentFile = os.path.join(stcpath, cfg.COMMENT_FILENAME)
    postFileFiltered = postFile + cfg.FILTER_POSTFIX
    commentFileFiltered = commentFile + cfg.FILTER_POSTFIX
#    print postFileFiltered
    vocab, postIndexs, commentIndexs = cut2index(postFileFiltered, commentFileFiltered)
    vocab = vocab + ['#END#']
    #for indexs in postIndexs:
    #    print ' '.join(str(x) for x in indexs)

    maxFeatures = len(vocab) + 1
    maxPostLen = max(map(len, (x for x in postIndexs)))
    maxCommentLen = max(map(len, (x for x in commentIndexs)))
    maxlen = max(maxPostLen, maxCommentLen)

    X = pad_sequences(postIndexs, maxlen)
    Y = pad_sequences(commentIndexs, maxlen)


    print 'after padd'
    #for indexs in X:
    #    print 'lenindex: ', len(indexs), ' '.join(str(x) for x in indexs)
    #xs = np.asarray(X)
    #Y = map(lambda x: map(to_one_hot, x), Y)
    #ys = np.asarray(Y)
    #print 'maxfeature, maxlen: ',  maxFeatures, maxlen
    #print("XS Shape: ", xs.shape)
    #print("YS Shape: ", ys.shape)
    #seq2seq(xs, ys, maxFeatures, maxlen)
    batchSeq2seq(X, Y, maxFeatures, maxlen)

