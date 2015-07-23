#! /usr/bin/env python2.7
#coding=utf-8
#filename: synonymsTest.py
import sys
sys.path.append('../')
import core.synonyms as syno

def testConstruct():
    synos = syno.Synonyms()
    synos.constructSynonymsDict()

def testReadSynomys():
    synos = syno.Synonyms()
    synos.readSynonyms()

def testSynoIndex():
    synos = syno.Synonyms()
    synos.constructSynoymsIndex()

def testQuerySyno():
    word = '姑娘'
    word = word.decode('utf-8')
    synos = syno.Synonyms()
    synos.constructSynoymsIndex()
    results = synos.querySynoyms(word)
    print word
    for res in results:
        print '---', res

if __name__ == '__main__':
    #testConstruct()
    #testReadSynomys()
    #testSynoIndex()
    testQuerySyno()

