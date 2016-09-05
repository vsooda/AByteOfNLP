#! /usr/bin/env python2.7
#coding=utf-8
#filename: tts_pinyin.py
import sys
sys.path.append('../test')
#import test
import  _init_paths
import jieba
import time
from config import cfg
import os
import glob
from os import listdir
from os.path import isfile, join
#import pinyin
import zh_pinyin as pinyin
import re

'''
for give a directory, then change the files in the dir to pinyin, and save the file to a second dir
'''

#read the file, change to pinyin then save the file
def change2pinyin(from_file, to_file, punt_dict):
    print from_file, to_file
    ffrom = open(from_file, 'r')
    words = ffrom.readline()
    print words
    #words = words.decode("utf-8")
    #这里转化为utf8之所以可转可不转是因为在获取拼音的代码内部有做转化utf8
    #jieba内部也有对字符串进行转换的代码，所以可以直接输入utf8. 但是实际上在处理的时候都是unicode
    han_pinyin = pinyin.get(words, ' ')
    res = []
    for char in han_pinyin:
        #res.join(punt_dict.get(char, char))
        #ret = punt_dict.get(char, char).encode('utf-8')
        ret = punt_dict.get(char, char)
        #res.join(ret)
        res = res + [ret]
        print char, ret
    res = ''.join(res)
    print han_pinyin, "-->", res
    #temp = han_pinyin.decode("utf8")
    #res = re.sub("[\.\!\/_,$%^*(+\"\']+|[+——！，。？、~@#￥%……&*（）]+".decode("utf8"), ",".decode("utf8"),temp)
    #han_pinyin = pinyin.filter_zh_punc(han_pinyin)
    #print res
    fto = open(to_file, 'w')
    #fto.write(han_pinyin)
    fto.write(res)
    ffrom.close()
    fto.close()



def dump_pinyin_dict(dict_name):
    fout = open('pinyin_key.txt', 'w')
    words = []
    with open(dict_name) as f:
        for line in f:
            k, v = line.strip().split('\t')
            w = v.lower().split(" ")[0]
            words.append(w)

    words = list(set(words))
    for w in words:
        fout.write(w)
        fout.write('\n')


def change_han_pinyin_dir(from_dir, to_dir, punt_dict):
    filenames = [f for f in listdir(from_dir) if isfile(join(from_dir, f)) ]
    for f in filenames:
        to_file = os.path.join(to_dir, f)
        from_file = os.path.join(from_dir, f)
        change2pinyin(from_file, to_file, punt_dict)


def test_punt_dict(punt_path):
    punt_dict = {}
    with open(punt_path) as f:
        for line in f:
            print line.strip()
            k, v = line.strip().split(' ')
            punt_dict[k] = v
            print k, v
    print punt_dict.get('。')

def change_dict_format(dict_path):
    pinyin_dict = {}
    with open(dict_path) as f:
        for line in f:
            k, v = line.strip().split('\t')
            pinyin_dict[k] = v.lower().split(" ")[0]
            #print k, v
            print unichr(int(k, 16)), v


def transcript_pinyin(from_file, to_file):
    print from_file, to_file
    ffrom = open(from_file, 'r')
    fto = open(to_file, 'w')
    lines = ffrom.readlines()
    linenum = 0
    for words in lines:
        print words
        han_pinyin = pinyin.get(words, ' ')

        fto.write(str(linenum)+'\n')
        fto.write(words)
        fto.write(han_pinyin)
        linenum = linenum + 1
        #res = []
        #for w in words:
        #  wpy = pinyin.get(w, ' ')
        #  temp = [w] + [wpy]
        #  res = res + temp
        #fto.write(res)
    ffrom.close()
    fto.close()

def change_han_pinyin_test():
    root_dir = cfg.ROOT_DIR
    save_path = os.path.join(root_dir, 'data/tts')
    tts_text = os.path.join(root_dir, "data/tts/text/utf")
    punt_dict = {}
    punt_path = os.path.join(root_dir, "data/review/punt_dict.txt")
    with open(punt_path) as f:
        for line in f:
            k, v = line.decode('utf-8').strip().split(' ')
            punt_dict[k] = v.strip()
    #print ord(k)
    from_file = os.path.join(root_dir, 'data/text.txt')
    to_file = os.path.join(root_dir, 'data/text_res1.txt')
    transcript_pinyin(from_file, to_file)
    change_han_pinyin_dir(tts_text, save_path, punt_dict)

def dump_pinyin_dict_test():
    root_dir = cfg.ROOT_DIR
    pinyinDict = os.path.join(root_dir, 'data/pinyin.txt')
    dump_pinyin_dict(pinyinDict)

def change_pinyin_dict_test():
    root_dir = cfg.ROOT_DIR
    pinyinDict = os.path.join(root_dir, 'data/pinyin.txt')
    change_dict_format(pinyinDict)

#filter out not use pinyin_word: not in pinyin_dict; all right;
def mix_pinyin_word_dict(pinyin_path, pinyin_word_path, save_name):
    pinyin_dict = {}
    with open(pinyin_path) as f:
        for line in f:
            k, v = line.decode('utf-8').strip().split('\t')
            pinyins = v.lower().split(" ")
            #if (len(pinyins) > 1) :
            han = unichr(int(k, 16))
            pinyin_dict[han] = pinyins
            #print  han, " ".join(pinyins)
    f.close()
    #for han, pinyins in pinyin_dict.items():
    #    print han, pinyins
    mix_lines = []
    with open(pinyin_word_path) as f:
        for line in f:
            line = line.decode('utf-8').strip()
            k, v = line.split(':')
            k = k.strip()
            v = v.strip()
            save_flag = True
            all_default = True
            pinyinss = ''
            for i in range(len(k)):
                han = k[i]
                line_pinyins = v.split(" ")
                pinyin = pinyin_dict.get(han, None)
                if pinyin is not None:
                    pinyinss = pinyinss + pinyin[0]
                    if pinyin[0] != line_pinyins[i]: #is the same with the default pinyin
                        all_default = False
                        if line_pinyins[i] not in pinyin:
                            print "not in list:break it", han, line_pinyins[i], 'in pinyin list: ', line, ' '.join(x for x in pinyin)
                            save_flag = False # not in pinyin list
                            break
                else:
                    print "can not find pinyin for ", han, pinyin
                    save_flag = False
                    break
            if save_flag and not all_default:
                print 'saving', line, pinyinss
                mix_lines.append(line)
            else:
                print 'no saving', line, pinyinss
    f.close()

    with open(save_name, 'w') as f:
        for line in  mix_lines:
            f.write(line)
            f.write('\n')
    f.close()

# read the pinyin dict and pinyin_word;remove the useless pinyin_word
def mix_pinyin_word_dict_test():
    root_dir = cfg.ROOT_DIR
    pinyin_path = os.path.join(root_dir, 'data/pinyin.txt')
    pinyin_word_path = os.path.join(root_dir, 'data/pinyin_word.txt')
    save_name = "mix_pinyin_word.txt"
    mix_pinyin_word_dict(pinyin_path, pinyin_word_path, save_name)


if __name__ == '__main__':
    #use glob can list files very easy. but need to cut the path
    #print glob.glob("/home/sooda/data/tts_data/text/*.txt")
    #test_punt_dict(punt_path)
    #change_han_pinyin_test()
    change_pinyin_dict_test()
    #mix_pinyin_word_dict_test()

