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
import pinyin
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

if __name__ == '__main__':
  #use glob can list files very easy. but need to cut the path
  #print glob.glob("/home/sooda/data/tts_data/text/*.txt")
  root_dir = cfg.ROOT_DIR
  save_path = os.path.join(root_dir, 'data/tts')
  tts_text = "/home/sooda/data/tts_data/text/utf"
  punt_dict = {}
  punt_path = os.path.join(root_dir, "data/review/punt_dict.txt")
  with open(punt_path) as f:
    for line in f:
      k, v = line.decode('utf-8').strip().split(' ')
      punt_dict[k] = v.strip()
      #print ord(k)
      print k, v


  #change_han_pinyin_dir(tts_text, save_path, punt_dict)
  #test_punt_dict(punt_path)
  dump_pinyin_dict("/home/sooda/data/pinyin.txt")
