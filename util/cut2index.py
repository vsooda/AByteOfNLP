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
from charset_type import *


def buildWordVocab(postLists, commentLists, wordCountThreshold = 5):
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
    stcpath = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH)
    vocabfile = os.path.join(stcpath, 'repos/vocab')
    wordcountfile = os.path.join(stcpath, 'wordcount.pkl')
    print 'save vocab file ', vocabfile

    fvocab = open(vocabfile, 'w')
    fvocab.write("#START# \n")
    fvocab.write("#END# \n")
    fvocab.write("#UNK# \n")
    for v in vocab:
        fvocab.write(v+'\n')

    print 'filtered words from %d to %d in %.2fs' % (len(wordCounts), len(vocab), time.time() - t0)
    pickle.dump(wordCounts, open(wordcountfile, 'wb'))

    return vocab

def buildWordIndex(vocab):
    #原本python代码中， start和end的id是0，可能会和pad产生误会？
    ixtoword = {}
    #ixtoword[0] = '#END#'
    wordtoix = {}
    #wordtoix['#START#'] = 0
    wordtoix["#START#"] = 1
    wordtoix["#END#"] = 2
    wordtoix["#UNK#"] = 3
    ixtoword[1] = "#START#"
    ixtoword[2] = "#END#"
    ixtoword[3] = "#UNK#"

    ix = 4
    for w in vocab:
        wordtoix[w] = ix
        ixtoword[ix] = w
        ix += 1
    #ixtoword[ix] = 'UNK'
    #wordtoix['#UNK#'] = ix
    #ixtoword[ix+1] = '#EOS#'
    #wordtoix['#EOS#'] = ix+1

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
        #indexs = [vocabSize] + [word2ix[w] for w in words if w in word2ix ]
        #torch translator
        indexs =[word2ix[w] if w in word2ix else 3 for w in reversed(words)]
        #print ', '.join(words)
        #print ' '.join(str(x) for x in indexs)
        postIndexs.append(indexs)
    for words in commentLists:
        indexs =[word2ix[w] if w in word2ix else 3 for w in words]
        indexs = [1] + indexs + [2]
        #print ' '.join(words)
        #print ' '.join(str(x) for x in indexs)
        commentIndexs.append(indexs)

    return postIndexs, commentIndexs

def writeIndexFile(postIndexName, postIndexs, commentIndexName, commentIndexs):
    print 'writing index file ', len(postIndexs), postIndexName, commentIndexName
    assert(len(postIndexs) == len(commentIndexs))
    fpostIndex = open(postIndexName, 'w')
    maxlen = 20
    endsysbol = 2
    for indexs in postIndexs:
        if len(indexs) > maxlen:
            #print "excees max len"
            #endsysbol = indexs[len(indexs) - 1]
            indexs = indexs[:maxlen-1] + [endsysbol]
            #print indexs
        text = ' '.join(str(x) for x in indexs) + '\n'
        fpostIndex.write(text)
    fcommentIndex = open(commentIndexName, 'w')
    for indexs in commentIndexs:
        if len(indexs) > maxlen:
            #endsysbol = indexs[len(indexs) - 1]
            indexs = indexs[:maxlen-1] + [endsysbol]
            #indexs = indexs[:maxlen]
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


def segment_chinese_single(seglist):
    res = []
    for word in seglist:
        word = word.decode("utf-8")
        temp = []
        if len(word) > 1:
            is_all_chinese = True
            for w in word:
                #print "www: ", w
                if not is_chinese(w):
                    is_all_chinese = False
                    break
            if is_all_chinese:
                for w in word:
                   temp = temp + [w]
            else:
                print word, " not all chinese"
                temp = [word]
        else:
            temp = [word]
        #print word, " segword: ", temp, " ", temp[0]
        res = res + temp
    return res


def segment_word(post_lines, comment_lines):
    postLists = []
    for line in post_lines:
        line = line.strip()
        seglist = jieba.cut(line)
        segs = segment_chinese_single(seglist)
        #segs = []
        #for w in seglist:
        #    segs.append(w)
        #print "line result: ", segs
        postLists.append(segs)

    commentLists = []
    for line in comment_lines:
        line = line.strip()
        seglist = jieba.cut(line)
        segs = segment_chinese_single(seglist)
        commentLists.append(segs)

    return postLists, commentLists

def segment_syllable(post_lines, comment_lines):
    postLists = []
    for line in post_lines:
        line = line.strip()
        line = unicode(line, "utf-8") # must convert to utf8 for cutting single chinese char
        segs = []
        for word in line:
            print word
            segs.append(word)
        postLists.append(segs)

    commentLists = []
    for line in comment_lines:
        line = line.strip()
        line = unicode(line, "utf-8")
        segs = []
        for word in line:
            segs.append(word)
        commentLists.append(segs)

    return postLists, commentLists


#generator new file which every word present with id
def cut2index(postFilename, commentFilename):
    fpost = open(postFilename)
    fcomment = open(commentFilename)
    postLines = fpost.readlines()
    commentLines = fcomment.readlines()
    #assert(len(postLines) == len(commentLines));
    #postLines = postLines.decode('utf-8')
    postLists, commentLists = segment_word(postLines, commentLines)
    #postLists, commentLists = segment_syllable(postLines, commentLines)

    print len(postLists)
    print len(commentLists)
    print ', '.join(postLists[0])
    vocab = buildWordVocab(postLists, commentLists)
    ix2word, word2ix = buildWordIndex(vocab)
    postIndexs, commentIndexs = buildSentenceIndex(postLists, commentLists, word2ix)
    for indexs in postIndexs:
        print ' '.join(ix2word[x] for x in indexs)
    #for indexs in commentIndexs:
    #    print ' '.join(ix2word[x] for x in indexs)

    postSegName = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH, cfg.POST_FILENAME) + cfg.SEG_POSTFIX
    commentSegName = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH, cfg.COMMENT_FILENAME) + cfg.SEG_POSTFIX
    writeSegFile(postSegName, postLists, commentSegName, commentLists)

    postIndexName = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH, cfg.POST_FILENAME) + cfg.INDEX_POSTFIX
    commentIndexName = os.path.join(cfg.ROOT_DIR, cfg.DATAPATH, cfg.COMMENT_FILENAME) + cfg.INDEX_POSTFIX
    writeIndexFile(postIndexName, postIndexs, commentIndexName, commentIndexs)

    maxindex = 1
    for indexs in postIndexs:
        if len(indexs) > maxindex:
            maxindex = len(indexs)
    for indexs in commentIndexs:
        if len(indexs) > maxindex:
            maxindex = len(indexs)
    print 'maxindex: ', maxindex

    return vocab, postIndexs, commentIndexs

