#! /usr/bin/env python2.7
#coding=utf-8
#filename: synonyms.py

class Synonyms:
    def __init__(self):
        print 'synonyms'

    def construct_synonyms_dict(self):
        pfile = open('../data/review/tyccl.txt', 'r')
        syno_index = open('../data/review/synoindex.txt', 'wb+')
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
                syno_index.write(word)
                for sim in wordsets:
                    if word != sim:
                        syno_index.write(' ' + sim)
                syno_index.write('\n')

    def read_synonyms(self):
        pfile = open('../data/review/synoindex.txt', 'r')
        txt = pfile.readlines()
        txt = ''.join(txt)
        txt = txt.strip()
        txt_datas = txt.decode('utf8').split('\n')
        pfile.close()
        #for words in txt_datas:
        #    print words
        return txt_datas

    def construct_synoyms_index(self):
        datas = self.read_synonyms()
        self.syno_index = {}
        for words in datas:
            words = words.strip()
            words = words.split(' ')
            #simWords = words[1:len(words)]
            #self.synoIndex[words[0]] = simWords
            if words[0] not in self.syno_index:
                self.syno_index[words[0]] = []
            self.syno_index[words[0]] = self.syno_index[words[0]] + words

        #for k, v in self.synoIndex.items():
        #    print k
        #    for word in v:
        #        print '---', word

    def query_synoyms(self, word):
        if word not in self.syno_index:
            return [word]
        else:
            return self.syno_index[word]



