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
        #print(i, ' '.join(indexs))

    return vocab, postIndexs, commentIndexs

def seq_driver(vocab, postIndexs, commentIndexs):
    vocab = ['0'] + vocab + ['UNK', 'END']
    #the first feature is none. this feature will be problem in the last full connect layer??

    max_features = len(vocab)
    #for i in range(max_features):
    #    print i, vocab[i]

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
    seq2seq(xs, ys, max_features, maxlen, vocab)

def seq_batch_driver(X, Y, max_features, maxlen):
    batchSeq2seq(X, Y, max_features, maxlen)


def cache_driver():
    root_dir = cfg.ROOT_DIR
    vocabfile = os.path.join(root_dir, 'data/cache/vocab')
    postfile = os.path.join(root_dir, 'data/cache/post')
    commentfile = os.path.join(root_dir, 'data/cache/comment')
    print vocabfile
    vocab, postIndexs, commentIndexs = readDataFile(vocabfile, postfile, commentfile)
    seq_driver(vocab, postIndexs, commentIndexs)

def total_test():
    stcpath = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH)
    postFile = os.path.join(stcpath, cfg.POST_FILENAME)
    commentFile = os.path.join(stcpath, cfg.COMMENT_FILENAME)
    postFileFiltered = postFile + cfg.FILTER_POSTFIX
    commentFileFiltered = commentFile + cfg.FILTER_POSTFIX
    vocab, postIndexs, commentIndexs = cut2index(postFileFiltered, commentFileFiltered)
    postIndexs = postIndexs[1:100]
    commentIndexs = commentIndexs[1:100]
    seq_driver(vocab, postIndexs, commentIndexs)

if __name__ == "__main__":
    #pickle_test()
    cache_driver()
    #total_test()

