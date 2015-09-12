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

#all return with list format
def readDataFile(vocabName, postIndexName, commentIndexName):
    fvocab = open(vocabName, 'r')
    vocabLines = fvocab.readlines()
    vocab = []
    for w in vocabLines:
        w = w.strip()
        vocab.append(w)

    fpostIndex = open(postIndexName, 'r')
    postIndexLines = fpostIndex.readlines()
    postIndexs = []
    for line in postIndexLines:
        line = line.strip()
        indexs = line.split(' ')
        int_indexs = [ int(x) for x in indexs]
        postIndexs.append(int_indexs)

    #for line in postIndexs:
    #    print(' '.join(str(x) for x in line))

    fcommentIndex = open(commentIndexName, 'r')
    commentIndexLines = fcommentIndex.readlines()
    commentIndexs = []
    i = 1
    for line in commentIndexLines:
        line = line.strip()
        indexs = line.split(' ')
        int_indexs = [ int(x) for x in indexs]
        commentIndexs.append(int_indexs)
        print(i, ' '.join(indexs))

    return vocab, postIndexs, commentIndexs

def seq_driver(xs, ys, max_features, maxlen):
    def to_one_hot(id):
        zeros = [0] * max_features
        zeros[id] = 1
        return zeros
    xs = np.asarray(xs)
    ys = map(lambda x: map(to_one_hot, x), ys)
    ys = np.asarray(ys)
    print("XS Shape: ", xs.shape)
    print("YS Shape: ", ys.shape)
    seq2seq(xs, ys, max_features, maxlen)

def seq_batch_driver(X, Y, max_features, maxlen):
    batchSeq2seq(X, Y, max_features, maxlen)



#def batch_test(X, Y, maxFetures, maxlen):
#    batchSeq2seq(X, Y, max_features, maxlen)
#
#def test(X, Y, max_features, maxlen):
#    #for indexs in X:
#    #    print 'lenindex: ', len(indexs), ' '.join(str(x) for x in indexs)
#    xs = np.asarray(X)
#    Y = map(lambda x: map(to_one_hot, x), Y)
#    ys = np.asarray(Y)
#    print 'maxfeature, maxlen: ',  max_features, maxlen
#    print("XS Shape: ", xs.shape)
#    print("YS Shape: ", ys.shape)
#    seq2seq(xs, ys, max_features, maxlen)

def cacheDriver():
    vocab, postIndexs, commentIndexs = readDataFile('cache/vocab', 'cache/comment', 'cache/post')
    vocab = vocab + ['UNK', '#END#']

    max_features = len(vocab) + 1
    maxPostLen = max(map(len, (x for x in postIndexs)))
    maxCommentLen = max(map(len, (x for x in commentIndexs)))
    maxlen = max(maxPostLen, maxCommentLen)

    X = pad_sequences(postIndexs, maxlen, 'int32', 'post', 'post')
    Y = pad_sequences(commentIndexs, maxlen, 'int32', 'post', 'post')
    #Y = pad_sequences(commentIndexs, maxlen)

    #print 'after padd'
    #batch_test(X, Y, max_features, maxlen)
    def to_one_hot(id):
        zeros = [0] * max_features
        zeros[id] = 1
        return zeros
    xs = np.asarray(X)
    Y = map(lambda x: map(to_one_hot, x), Y)
    ys = np.asarray(Y)
    print('maxfeature, maxlen: ',  max_features, maxlen)
    print("XS Shape: ", xs.shape)
    print("YS Shape: ", ys.shape)
    seq2seq(xs, ys, max_features, maxlen)

def total_test():
    stcpath = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH)
    postFile = os.path.join(stcpath, cfg.POST_FILENAME)
    commentFile = os.path.join(stcpath, cfg.COMMENT_FILENAME)
    postFileFiltered = postFile + cfg.FILTER_POSTFIX
    commentFileFiltered = commentFile + cfg.FILTER_POSTFIX
#    print postFileFiltered
    vocab, postIndexs, commentIndexs = cut2index(postFileFiltered, commentFileFiltered)
    vocab = vocab + ['UNK', '#END#']
    #for indexs in postIndexs:
    #    print ' '.join(str(x) for x in indexs)

    postIndexs = postIndexs[1:100]
    commentIndex = commentIndex[1:100]

    max_features = len(vocab) + 1
    maxPostLen = max(map(len, (x for x in postIndexs)))
    maxCommentLen = max(map(len, (x for x in commentIndexs)))
    maxlen = max(maxPostLen, maxCommentLen)

    X = pad_sequences(postIndexs, maxlen, 'int32', 'post', 'post')
    Y = pad_sequences(commentIndexs, maxlen, 'int32', 'post', 'post')
    #Y = pad_sequences(commentIndexs, maxlen)

    print 'after padd'
    #seq_batch_driver(X, Y, max_features, maxlen)
    seq_driver(X, Y, max_features, maxlen)

if __name__ == "__main__":
    #pickle_test()
    cacheDriver()

