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

def test_convert_transcript_id():
    root_dir = cfg.ROOT_DIR
    lexicon_file = os.path.join(root_dir, 'data/tts/zh_lexicon.dict')
    lexicon_dict, phone2pinyin = read_pinyin_transcript(lexicon_file)
    phoneset_file = os.path.join(root_dir, 'data/tts/phoneset.txt')
    phones_dict, id2phone = read_phoneset_map(phoneset_file)
    line = "……嗯?"
    transcript = convert_word_transcript(line, lexicon_dict)
    print transcript
    line_id = convert_transcript_id(transcript, phones_dict)
    print line_id
    line1 = '爹……让他走!!!不要伤他!爹……'
    transcript1 = convert_word_transcript(line1, lexicon_dict)
    print transcript1
    line_id1 = convert_transcript_id(transcript1, phones_dict)
    print line_id1
    triphone_list = generate_line_triphone(line_id1)
    print triphone_list


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
    save_id_file = False
    save_file = 'mini.id'
    if save_id_file:
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

# generator extend sentence id and save in the cache file
# it contains validation process
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
    assert len(confirm_cover_status) == len(confirm_cover_status2)

    #save the select top sentence id
    select_id_filename = os.path.join(root_dir, 'data/tts/select_id')
    fselectid = open(select_id_filename, 'w')
    fselectid.write(' '.join(str(x) for x in select_sentences_id))

# to test the select id if it is ok
# use the orig chinese data and the extend sentence id for extending
# compute the cover_status if its the same as the choose result..
def test_confirm_select_sentence():
    root_dir = cfg.ROOT_DIR
    lexicon_file = os.path.join(root_dir, 'data/tts/zh_lexicon.dict')
    lexicon_dict, phone2pinyin = read_pinyin_transcript(lexicon_file)
    phoneset_file = os.path.join(root_dir, 'data/tts/phoneset.txt')
    phones_dict, id2phone = read_phoneset_map(phoneset_file)
    word_name = os.path.join(root_dir, "data/tts/total.txt")
    orig_trans_lines = convert_file_word_transcripts(word_name, lexicon_dict)
    orig_lines_ids = convert_transciprt_lines_ids(orig_trans_lines, phones_dict)
    orig_triphone_list_list = generate_lines_triphone(orig_lines_ids)
    cover_status = construct_triphone_count(orig_triphone_list_list)
    print_cover_status(cover_status)
    orig_cover_status = cover_status

    #get line from sentence id file
    select_id_filename = os.path.join(root_dir, 'data/tts/select_id')
    fselect_id = open(select_id_filename, 'r')
    select_id_str = fselect_id.readline()
    fselect_id.close()
    select_ids = select_id_str.split()
    select_ids = [int(x) for x in select_ids]
    print select_ids
    extend_filename = os.path.join(root_dir, 'data/tts/mini_word.txt')
    fextend = open(extend_filename, 'r')
    extend_lines = fextend.readlines()
    fextend.close()
    extend_lines = [x.decode('utf-8').strip() for x in extend_lines]
    select_lines_sentences = [extend_lines[x] for x in select_ids]
    for line in select_lines_sentences:
        print line
    extend_lines_ids = convert_lines_word_transcripts_id(select_lines_sentences, lexicon_dict, phones_dict)
    extend_triphone_list_list = generate_lines_triphone(extend_lines_ids)
    do_extend_cover_ll(cover_status, extend_triphone_list_list)
    print len(cover_status)



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

def test_total_procedure():
    root_dir = cfg.ROOT_DIR
    #lexicon_filename = os.path.join(root_dir, 'data/tts/zh_lexicon.dict')
    #phoneset_filename = os.path.join(root_dir, 'data/tts/phoneset.txt')
    lexicon_filename = os.path.join(root_dir, 'data/tts/zh_lexicon176.dict')
    phoneset_filename = os.path.join(root_dir, 'data/tts/phoneset176.txt')
    #orig_filename = os.path.join(root_dir, "data/tts/total.txt")
    #orig_filename = os.path.join(root_dir, "data/tts/cslt.txt")
    orig_filename = os.path.join(root_dir, "data/tts/4k.txt")
    #extend_filename = os.path.join(root_dir, 'data/tts/mini_word.txt')
    #extend_filename = os.path.join(root_dir, 'data/tts/mini_extract.txt')
    #extend_filename = os.path.join(root_dir, 'data/tts/extract.txt')
    extend_filename = os.path.join(root_dir, 'data/tts/sentences.txt')
    save_filename = os.path.join(root_dir, 'data/tts/save.txt')
    extend_dataset(orig_filename, extend_filename, save_filename, lexicon_filename, phoneset_filename, 30, 110)

def test_confirm_total_procedure():
    root_dir = cfg.ROOT_DIR
    lexicon_filename = os.path.join(root_dir, 'data/tts/zh_lexicon.dict')
    phoneset_filename = os.path.join(root_dir, 'data/tts/phoneset.txt')
    orig_filename = os.path.join(root_dir, "data/tts/total.txt")
    extend_save_filename = os.path.join(root_dir, 'data/tts/save.txt')
    confirm_extend_dataset(orig_filename, extend_save_filename, lexicon_filename, phoneset_filename)

def test_get_average_length():
    root_dir = cfg.ROOT_DIR
    filename = os.path.join(root_dir, "data/tts/total.txt")
    average_length = get_average_length(filename)
    print average_length


def test_file_sentences():
    root_dir = cfg.ROOT_DIR
    filename = os.path.join(root_dir, "data/tts/pfdsj.txt")
    sentences = extract_file_sentences(filename)
    sentences = filter_punct(sentences)
    save_name = os.path.join(root_dir, 'data/tts/sentences.txt')
    write_lines_file(save_name, sentences)

def test_file_sentences_batch():
    root_dir = cfg.ROOT_DIR
    filename = os.path.join(root_dir, "data/tts/pfdsj.txt")
    total_sentences = []
    dirname = os.path.join(root_dir, 'data/tts/minzhu/')
    for root, dirs, files in os.walk(dirname):
        for name in files:
            filename = os.path.join(root, name)
            print filename
            sentences = extract_file_sentences(filename)
            total_sentences = total_sentences + sentences
    #total_sentences = filter_double_quotation(total_sentences)
    total_sentences = filter_punct(total_sentences)

    save_name = os.path.join(root_dir, 'data/tts/sentences.txt')
    write_lines_file(save_name, total_sentences)


def splitStringFull(sh, st):
    ls = sh.split(st)
    print ls
    lo = []
    start = 0
    for l in ls:
        if not l:
            continue
        k = st.find(l)
        llen = len(l)
        if k > start:
            tmp = st[start:k]
            lo.append(tmp)
            lo.append(l)
            start = k + llen
        else:
            lo.append(l)
            start = llen
    return lo


def test_splitStringFull():
    import re
    st="%%(c+dd+e+f-1523)%%7"
    sh=re.compile('[\+\-//\*\<\>\%\(\)]')
    li = splitStringFull(sh, st)
    print li

def test_find():
    #strings = 'adgaeaaeadf'
    strings = '你好。搞什么飞架阿。呵呵。'
    strings = strings.decode('utf-8').strip()
    #index = strings.find('e')
    index = strings.find('。')
    print index

    find_result = find_all(strings, '。'.decode('utf-8'))
    indexs = list(find_result) # transfer generator to list
    start = 0
    substring = []
    for index in indexs:
        substring.append(strings[start:index+1])
        start = index + 1
    if start < len(strings):
        substring.append(strings[start:len(strings)])
    for subs in substring:
        print subs

def test_filter_quotation():
    test_string1 = "搞什么飞机”".decode('utf-8')
    result1 = filter_quotation(test_string1)
    print test_string1
    print result1
    test_string2 = "“搞什么飞机”".decode('utf-8')
    result2 = filter_quotation(test_string2)
    print test_string2
    print result2



if __name__ == '__main__':
    #gen_test()
    #filter_test()
    #test_dir("/Users/sooda/nlp/AByteOfNLP/data/tts/juben")
    #test_get_average_length()
    #test_convert_transcript_id()
    #test_extract_converstion_batch()
    #test_convert_file_transcript()
    #test_string_format()
    #test_convert_file_transcript_id()
    #test_generate_line_triphone()
    #test_convert_han_file_triphone()
    #test_triphoneid_to_phones()
    #test_extend_triphone()
    #test_shuffle()
    #test_sentences_extend()
    #test_confirm_select_sentence()
    #test_filter_quotation()
    test_total_procedure()
    #test_confirm_total_procedure()
    #test_file_sentences()
    #test_file_sentences_batch()
    #test_splitStringFull()
    #test_find()
