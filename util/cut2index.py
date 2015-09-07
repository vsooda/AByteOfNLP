#! /usr/bin/env python2.7
#coding=utf-8
#filename: cut2index.py
import sys
import jieba
import time
from config import cfg
import cPickle as pickle
import _init_paths
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
    fvocab = open('vocab', 'w')
    for v in vocab:
        fvocab.write(v+'\n')

    print 'filtered words from %d to %d in %.2fs' % (len(wordCounts), len(vocab), time.time() - t0)
    pickle.dump(wordCounts, open('wordcount.pkl', 'wb'))

    return vocab

def buildWordIndex(vocab):
    ixtoword = {}
    #ixtoword[0] = '#END#'
    wordtoix = {}
    #wordtoix['#START#'] = 0
    ix = 1
    for w in vocab:
        wordtoix[w] = ix
        ixtoword[ix] = w
        ix += 1
    ixtoword[ix] = '#END#'
    wordtoix['#START#'] = ix

    return ixtoword, wordtoix

def buildSentenceIndex(postLists, commentLists, word2ix):
    postSents = []
    commentSents = []
    print 'sentenct indexing'
    print len(postLists)
    postIndexs = []
    commentIndexs = []

    vocabSize = len(word2ix)
    #print len(postLists[0])
    #just ingnore the symbol which is not in the vocab
    for words in postLists:
        indexs = [vocabSize] + [word2ix[w] for w in words if w in word2ix ]
        #print ', '.join(words)
        #print ' '.join(str(x) for x in indexs)
        postIndexs.append(indexs)
    for words in commentLists:
        indexs =[word2ix[w] for w in words if w in word2ix ] +[vocabSize]
        #print ' '.join(words)
        #print ' '.join(str(x) for x in indexs)
        commentIndexs.append(indexs)

    return postIndexs, commentIndexs

def writeIndexFile(postIndexName, postIndexs, commentIndexName, commentIndexs):
    print 'writing index file ', len(postIndexs), postIndexName, commentIndexName
    assert(len(postIndexs) == len(commentIndexs))
    fpostIndex = open(postIndexName, 'w')
    for indexs in postIndexs:
        text = ' '.join(str(x) for x in indexs) + '\n'
        fpostIndex.write(text)
    fcommentIndex = open(commentIndexName, 'w')
    for indexs in commentIndexs:
        text = ' '.join(str(x) for x in indexs) + '\n'
        fcommentIndex.write(text)

def writeSegFile(postSegName, postLists, commentSegName, commentLists):
    fpostSeg = open(postSegName, 'w')
    for words in postLists:
        text = ' '.join(words) + '\n'
        fpostSeg.write(text)
    fcommentSeg = open(commentSegName, 'w')
    for words in commentLists:
        text = ' '.join(words) + '\n'
        fcommentSeg.write(text)



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
    postIndexs, commentIndexs = buildSentenceIndex(postLists, commentLists, word2ix)
    for indexs in postIndexs:
        print ' '.join(ix2word[x] for x in indexs)
    for indexs in commentIndexs:
        print ' '.join(ix2word[x] for x in indexs)
    #for indexs in commentIndexs:
    #    print ' '.join(str(x) for x in indexs)

    postSegName = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH, cfg.POST_FILENAME) + cfg.SEG_POSTFIX
    commentSegName = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH, cfg.COMMENT_FILENAME) + cfg.SEG_POSTFIX
    writeSegFile(postSegName, postLists, commentSegName, commentLists)

    postIndexName = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH, cfg.POST_FILENAME) + cfg.INDEX_POSTFIX
    commentIndexName = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH, cfg.COMMENT_FILENAME) + cfg.INDEX_POSTFIX
    writeIndexFile(postIndexName, postIndexs, commentIndexName, commentIndexs)

