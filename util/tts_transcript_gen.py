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

def strQ2B(ustring):
    """全角转半角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 12288:                              #全角空格直接转换
            inside_code = 32
        elif (inside_code >= 65281 and inside_code <= 65374): #全角字符（除空格）根据关系转化
            inside_code -= 65248

        rstring += unichr(inside_code)
    return rstring

def strB2Q(ustring):
    """半角转全角"""
    rstring = ""
    for uchar in ustring:
        inside_code=ord(uchar)
        if inside_code == 32:                                 #半角空格直接转化
            inside_code = 12288
        elif inside_code >= 32 and inside_code <= 126:        #半角字符（除空格）根据关系转化
            inside_code += 65248

        rstring += unichr(inside_code)
    return rstring

def filter_test():
    #dialogPattern = re.compile(r'["“](.*?)["”]');
    dialogPattern = re.compile(r'".*?"');
    #dialogPattern = re.compile(r'\“.*?\”');
    line = '“搞什么" "飞机啊”'
    line = line.replace('“', '"').replace('”', '"')
    line = line.decode('utf-8').strip()
    print line
    match = dialogPattern.match(line)
    if match:
        print match.group()
    else:
        print "none"

def extract_conversation_text(text_file):
    ftext = open(text_file)
    lines = ftext.readlines()
    index = 0
    #dialogPattern = re.compile(r'["“](.*?)["”]');
    converstion_lines = []
    dialogPattern = re.compile(r'".*?"');
    for line in lines:
        line = line.decode('utf-8').strip().replace('“', '"').replace('”', '"')
        line = strQ2B(line)
        if len(line) < 10:
            continue
        match = dialogPattern.match(line)
        if match:
            match_str = match.group()
            if len(match_str) > 5:
                match_str = match_str.replace('"', '')
                converstion_lines.append(match_str)
    ftext.close()
    return converstion_lines


def test_dir(dirname):
    for root, dirs, files in os.walk(dirname):
        for name in files:
            print os.path.join(root, name)

def gen_test():
    conversations = extract_conversation_text("/Users/sooda/nlp/AByteOfNLP/data/tts/juben/hzgg2.txt")
    for conversation in conversations:
        print conversation

def extract_conversation_batch(dirname):
    fconversations = open("extract.txt", "w")
    for root, dirs, files in os.walk(dirname):
        for name in files:
            filename = os.path.join(root, name)
            print filename
            conversations = extract_conversation_text(filename)
            for conversation in conversations:
                #print conversation
                fconversations.write(conversation)
                fconversations.write("\n")



if __name__ == '__main__':
    extract_conversation_batch("/Users/sooda/nlp/AByteOfNLP/data/tts/juben")
   #gen_test()
   # filter_test()
   #test_dir("/Users/sooda/nlp/AByteOfNLP/data/tts/juben")

