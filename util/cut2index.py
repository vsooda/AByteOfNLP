#! /usr/bin/env python2.7
#coding=utf-8
#filename: cut2index.py
import sys
import jieba
import time
import cPickle as pickle
sys.path.append('../')
import os


def buildWordVocab(postLists, commentLists, wordCountThreshold = 2):
    wordCounts = {}
    nsents = 0
    t0 = time.time()
    for words in postLists:
        for w in words:
            wordCounts[w] = wordCounts.get(w, 0) + 1
    for words in commentLists:
        for w in words:
            wordCounts[w] = wordCounts.get(w, 0) + 1
    #for k, v in wordCounts.items():
    #    print k, v
    vocab = [w for w in wordCounts if wordCounts[w] >= wordCountThreshold]
    print 'filtered words from %d to %d in %.2fs' % (len(wordCounts), len(vocab), time.time() - t0)
    pickle.dump(wordCounts, open('wordcount.pkl', 'wb'))

    return vocab

def buildWordIndex(vocab):
    ixtoword = {}
    ixtoword[0] = '.'
    wordtoix = {}
    wordtoix['#START#'] = 0
    ix = 1
    for w in vocab:
        wordtoix[w] = ix
        ixtoword[ix] = w
        ix += 1
    return ixtoword, wordtoix

def buildSentenceIndex(postLists, commentLists, word2ix):
    postSents = []
    commentSents = []
    print 'sentenct indexing'
    print len(postLists)
    #print len(postLists[0])
    #just ingnore the symbol which is not in the vocab
    for words in postLists:
        indexs = [0] + [word2ix[w] for w in words if w in word2ix ]
        print ', '.join(words)
        for index in indexs:
            print index
    for words in commentLists:
        indexs =[word2ix[w] for w in words if w in word2ix ] + [0]
        print ', '.join(words)
        for index in indexs:
            print index

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
        segs = []
        for word in seglist:
            segs.append(word)
        postLists.append(segs)

    commentLists = []
    for line in commentLines:
        line = line.strip()
        seglist = jieba.cut(line)
        segs = []
        for word in seglist:
            segs.append(word)
        commentLists.append(segs)

    print len(postLists)
    print len(commentLists)
    print ', '.join(postLists[0])
    vocab = buildWordVocab(postLists, commentLists)
    ix2word, word2ix = buildWordIndex(vocab)
    buildSentenceIndex(postLists, commentLists, word2ix)


