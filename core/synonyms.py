#! /usr/bin/env python2.7
#coding=utf-8
#filename: synonyms.py

class Synonyms:
    def __init__(self):
        print 'synonyms'

    def constructSynonymsDict(self):
        pfile = open('../data/tyccl.txt', 'r')
        synoIndex = open('../data/synoindex.txt', 'wb+')
        txt = pfile.readlines()
        txt = ''.join(txt)
        txt = txt.strip()
        txt_datas = txt.decode('utf8').split('\n')
        pfile.close()
        print txt_datas[10000]
        for row in txt_datas:
            row = row.strip()
            wordsets = row.split(' ')
            desc = wordsets[0]
            lev = desc[len(desc) -1]
            print row
            if lev != '=':
                continue
            print lev
            wordsets = wordsets[1:len(wordsets)]
            for word in wordsets:
                print '---', word
                synoIndex.write(word)
                for sim in wordsets:
                    if word != sim:
                        synoIndex.write(' ' + sim)
                synoIndex.write('\n')

    def readSynonyms(self):
        pfile = open('../data/synoindex.txt', 'r')
        txt = pfile.readlines()
        txt = ''.join(txt)
        txt = txt.strip()
        txt_datas = txt.decode('utf8').split('\n')
        pfile.close()
        #for words in txt_datas:
        #    print words
        return txt_datas

    def constructSynoymsIndex(self):
        datas = self.readSynonyms()
        self.synoIndex = {}
        for words in datas:
            words = words.strip()
            words = words.split(' ')
            #simWords = words[1:len(words)]
            #self.synoIndex[words[0]] = simWords
            self.synoIndex[words[0]] = words

        #for k, v in self.synoIndex.items():
        #    print k
        #    for word in v:
        #        print '---', word

    def querySynoyms(self, word):
        if word not in self.synoIndex:
            return [word]
        else:
            return self.synoIndex[word]



