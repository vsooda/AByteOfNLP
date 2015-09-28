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

'''
for give a directory, then change the files in the dir to pinyin, and save the file to a second dir
'''

#read the file, change to pinyin then save the file
def change2pinyin(from_file, to_file):
  print from_file, to_file
  ffrom = open(from_file, 'r')
  words = ffrom.readline()
  print words
  han_pinyin = pinyin.get(words, ' ')
  fto = open(to_file, 'w')
  fto.write(han_pinyin)
  ffrom.close()
  fto.close()




def change_han_pinyin_dir(from_dir, to_dir):
  filenames = [f for f in listdir(from_dir) if isfile(join(from_dir, f)) ]
  for f in filenames:
    to_file = os.path.join(to_dir, f)
    from_file = os.path.join(from_dir, f)
    change2pinyin(from_file, to_file)



if __name__ == '__main__':
  #use glob can list files very easy. but need to cut the path
  #print glob.glob("/home/sooda/data/tts_data/text/*.txt")
  root_dir = cfg.ROOT_DIR
  save_path = os.path.join(root_dir, 'data/tts')
  tts_text = "/home/sooda/data/tts_data/text/utf"
  change_han_pinyin_dir(tts_text, save_path)
