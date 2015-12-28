#! /usr/bin/env python2.7
#coding=utf-8
#filename: tts_transcript_gen_test.py
import sys
import  _init_paths
import jieba
import time
from config import cfg
import os
import glob
from os import listdir
from os.path import isfile, join
#import pinyin
import util.zh_pinyin as pinyin
import re
import random
from util.tts_transcript_gen import *


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


def test_dir(dirname):
    for root, dirs, files in os.walk(dirname):
        for name in files:
            print os.path.join(root, name)

def gen_test():
    conversations = extract_conversation_text("/Users/sooda/nlp/AByteOfNLP/data/tts/juben/hzgg2.txt")
    for conversation in conversations:
        print conversation

def test_convert_file_transcript():
    root_dir = cfg.ROOT_DIR
    lexicon_file = os.path.join(root_dir, 'data/tts/zh_lexicon.dict')
    lexicon_dict, phone2pinyin = read_pinyin_transcript(lexicon_file)
    word_name = os.path.join(root_dir, "data/tts/mini_word.txt")
    print word_name
    trans_lines = convert_file_word_transcripts(word_name, lexicon_dict)
    for line in trans_lines:
        print line

def test_convert_file_transcript_id():
    root_dir = cfg.ROOT_DIR
    lexicon_file = os.path.join(root_dir, 'data/tts/zh_lexicon.dict')
    lexicon_dict, phone2pinyin = read_pinyin_transcript(lexicon_file)
    word_name = os.path.join(root_dir, "data/tts/total.txt")
    #word_name = os.path.join(root_dir, "data/tts/mini_word.txt")
    trans_lines = convert_file_word_transcripts(word_name, lexicon_dict)
    phoneset_file = os.path.join(root_dir, 'data/tts/phoneset.txt')
    phones_dict, id2phone = read_phoneset_map(phoneset_file)
    lines_ids = convert_transciprt_lines_ids(trans_lines, phones_dict)
    #for line_ids in lines_ids:
    #    print ' '.join(str(x) for x in line_ids)
    save_file = 'mini.id'
    if save_file:
        f = open(save_file, 'w')
        for line_ids in lines_ids:
            f.write(' '.join(str(x) for x in line_ids))
            f.write('\n')

def test_convert_han_file_triphone():
    root_dir = cfg.ROOT_DIR
    lexicon_file = os.path.join(root_dir, 'data/tts/zh_lexicon.dict')
    lexicon_dict, phone2pinyin = read_pinyin_transcript(lexicon_file)
    word_name = os.path.join(root_dir, "data/tts/total.txt")
    #word_name = os.path.join(root_dir, "data/tts/mini_word.txt")
    trans_lines = convert_file_word_transcripts(word_name, lexicon_dict)
    phoneset_file = os.path.join(root_dir, 'data/tts/phoneset.txt')
    phones_dict, id2phone = read_phoneset_map(phoneset_file)
    lines_ids = convert_transciprt_lines_ids(trans_lines, phones_dict)
    lines = []
    for line_ids in lines_ids:
        lines.append(' '.join(str(x) for x in line_ids))
    triphone_list_list = generate_lines_triphone(lines)
    cover_status = construct_triphone_count(triphone_list_list)

    cover_status = sorted(cover_status.iteritems(), key=lambda d:d[1], reverse=True)
    print_cover_status(cover_status, id2phone, phone2pinyin)


def test_triphoneid_to_phones():
    root_dir = cfg.ROOT_DIR
    phoneset_file = os.path.join(root_dir, 'data/tts/phoneset.txt')
    phones_dict, id2phone = read_phoneset_map(phoneset_file)
    ids1 = "39-10-10"
    phones1 = triphoneid_to_phones(id2phone, ids1)
    print phones1
    ids2 = '0-20-0'
    phones2 = triphoneid_to_phones(id2phone, ids2)
    print phones2


def test_extend_triphone():
    root_dir = cfg.ROOT_DIR
    origin_id_filename = os.path.join(root_dir, 'data/tts/total.id')
    #extend_id_filename = os.path.join(root_dir, 'data/tts/extend.id')
    extend_id_filename = os.path.join(root_dir, 'data/tts/mini_extend.id')
    orig_triphone_list_list = get_triphone_listlist_idfile(origin_id_filename)
    cover_status = construct_triphone_count(orig_triphone_list_list)
    print_cover_status(cover_status)
    print len(cover_status)

    extend_triphone_list_list = get_triphone_listlist_idfile(extend_id_filename)
    #extend_cover_status = construct_triphone_count(extend_triphone_list_list)
    #print_cover_status(extend_cover_status)
    #print len(extend_cover_status)

    total_num = 0
    #need to shuffle the data and add 10 highest sentence every batch
    for triphone_list in extend_triphone_list_list:
        #num = compute_extend_cover_num(cover_status, triphone_list, True)
        #total_num = total_num + num
        score = compute_extend_cover_score(cover_status, triphone_list)
        print score
    print len(cover_status)

def test_sentences_extend():
    root_dir = cfg.ROOT_DIR
    origin_id_filename = os.path.join(root_dir, 'data/tts/total.id')
    #extend_id_filename = os.path.join(root_dir, 'data/tts/extend.id')
    extend_id_filename = os.path.join(root_dir, 'data/tts/mini_extend.id')
    orig_triphone_list_list = get_triphone_listlist_idfile(origin_id_filename)
    cover_status = construct_triphone_count(orig_triphone_list_list)
    print_cover_status(cover_status)
    orig_cover_status = cover_status
    print len(cover_status)

    extend_triphone_list_list = get_triphone_listlist_idfile(extend_id_filename)

    total_num = 0
    #need to shuffle the data and add 10 highest sentence every batch
    select_indicate = sentences_extend(cover_status, extend_triphone_list_list, 10, 20)
    print len(cover_status)
    confirm_cover_status = orig_cover_status
    confirm_select_sentence_extend(confirm_cover_status, extend_triphone_list_list, select_indicate)
    print len(confirm_cover_status)

    fextend = open(extend_id_filename, 'r')
    orig_id_lines = fextend.readlines()
    select_sentences_id = [x for x in range(len(select_indicate)) if select_indicate[x] == 1]
    select_sentences = [orig_id_lines[index].decode('utf-8').strip() for index in select_sentences_id]

    #confirm test 2
    confirm_cover_status2 = orig_cover_status
    confirm_triphone_list_list2 = generate_lines_triphone(select_sentences)
    do_extend_cover_ll(confirm_cover_status2, confirm_triphone_list_list2)
    print len(confirm_cover_status2)






def test_lexicon_dict():
    root_dir = cfg.ROOT_DIR
    lexicon_file = os.path.join(root_dir, 'data/tts/zh_lexicon.dict')
    lexicon_dict, phone2pinyin = read_pinyin_transcript(lexicon_file)
    for k, v in lexicon_dict.items():
        print k, v

def test_phoneset_dict():
    root_dir = cfg.ROOT_DIR
    phoneset_file = os.path.join(root_dir, 'data/tts/phoneset.txt')
    phones_dict = read_phoneset_map(phoneset_file)
    for k, v in phones_dict.items():
        print k, v

def test_extract_converstion_batch():
    root_dir = cfg.ROOT_DIR
    juben_dir = os.path.join(root_dir, 'data/tts/juben')
    extract_conversation_batch(juben_dir)

def compute_cover():
    print 'a'

#warning the first and the end with have 2-element  model string
def test_string_format():
    a = 10
    b = 20
    c = 30
    coverstr = "%d-%d-%d" % (19, 20, 21)
    print coverstr

def test_generate_line_triphone():
    print 'test case 1 '
    line1 = "10 20 30 50 60 70"
    triphones1 = generate_line_triphone(line1)
    for triphone in triphones1:
        print triphone

    print 'test case 2'
    line2 = '10'
    triphones2 = generate_line_triphone(line2)
    for triphone in triphones2:
        print triphone

    print 'test case 3'
    line3 = '10 20'
    triphones3 = generate_line_triphone(line3)
    for triphone in triphones3:
        print triphone

def test_shuffle():
    a = range(1, 10)
    random.shuffle(a)
    print a

if __name__ == '__main__':
    #gen_test()
    #filter_test()
    #test_dir("/Users/sooda/nlp/AByteOfNLP/data/tts/juben")
    #test_convert_file_transcript()
    #test_string_format()
    #test_convert_file_transcript_id()
    #test_generate_line_triphone()
    #test_convert_han_file_triphone()
    #test_triphoneid_to_phones()
    #test_extend_triphone()
    #test_shuffle()
    test_sentences_extend()
