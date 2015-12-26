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

def read_phoneset_map(filename):
    index = 1
    phonemap = {}
    id2phone = {}
    with open(filename) as f:
        for line in f:
            phone = line.decode('utf-8').strip();
            id2phone[index] = phone
            phonemap[phone] = index
            index = index + 1
    f.close()
    return phonemap, id2phone

def read_pinyin_transcript(filename):
    pinyin_transcript_dict = {}
    phone2pinyin = {}
    with open(filename) as f:
        for line in f:
            py, phones = line.decode('utf-8').strip().split('|')
            pinyin_transcript_dict[py] = phones;
            phones = phones.replace(" ", "")
            phone2pinyin[phones] = py
    f.close()
    return pinyin_transcript_dict, phone2pinyin

def convert_word_pinyin(line):
    han_pinyin = pinyin.get(line, ' ')
    return han_pinyin

def convert_word_transcript(line, lexicon_dict):
    trans = ""
    line = line.decode('utf-8').strip()
    if len(line) == 0:
        print "empty line"
    else:
        han_pinyin = convert_word_pinyin(line)
        pinyins = han_pinyin.split(" ")
        for py in pinyins:
            trans = trans + lexicon_dict.get(py, ' ') + " "
    return trans

def convert_lines_word_transcripts(lines, lexicon_dict):
    trans_lines = []
    for line in lines:
        trans_line = convert_word_transcript(line, lexicon_dict)
        trans_lines.append(trans_line)
    return trans_lines

def convert_lines_word_transcripts_id(lines, lexicon_dict, phone_dict):
    trans_lines = convert_lines_word_transcripts(lines, lexicon_dict)
    lines_ids = convert_transciprt_lines_ids(trans_lines, phone_dict)
    return lines_ids

def convert_file_word_transcripts(filename, lexicon_dict):
    f = open(filename, 'r')
    lines = f.readlines()
    print len(lines)
    trans_lines = convert_lines_word_transcripts(lines, lexicon_dict)
    f.close()
    return trans_lines

def convert_file_word_transcripts_id(filename, lexicon_dict, phone_dict):
    trans_lines = convert_file_word_transcripts(filename, lexicon_dict)
    lines_ids = convert_transciprt_lines_ids(trans_lines, phone_dict)
    return lines_ids

def convert_transcript_id(trans_line, phones_dict):
    ids = []
    #to split string with muitiple whitespace
    #phones = trans_line.strip().split(' ') #wrong
    #phones = re.split("\s+", trans_line.strip()) #ok
    phones = trans_line.split()
    for phone in phones:
        index = phones_dict.get(phone, 0)
        if index == 0:
            print index, phone
        ids.append(index)
    return ids

def convert_transciprt_lines_ids(trans_lines, phones_dict):
    lines_ids = []
    for line in trans_lines:
        ids = convert_transcript_id(line, phones_dict)
        lines_ids.append(ids)
    return lines_ids

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
    #word_name = os.path.join(root_dir, "data/tts/total.txt")
    word_name = os.path.join(root_dir, "data/tts/mini_word.txt")
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


def print_cover_status(cover_status, id2phone=None, phone2pinyin=None):
    cover_status = sorted(cover_status.iteritems(), key=lambda d:d[1], reverse=True)
    index = 0
    print "tirphone cover num: ", len(cover_status)
    for key, value in cover_status:
        if id2phone:
            triphone = triphoneid_to_phones(id2phone, key)
            if phone2pinyin:
                print phone2pinyin.get(triphone, triphone), value
            else:
                print triphone, value
        else:
            print key, value
        index = index + 1
        if index > 100:
            break


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


def triphoneid_to_phones(id2phone, triphoneid):
    ids = triphoneid.split('-')
    phones = ""
    for phoneid in ids:
        phone = id2phone.get((int(phoneid, 10)), '-')
        phones = phones + phone
    return phones

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

def construct_triphone_count(triphone_list_list):
    cover_status = {}
    total_triphone = 0
    for triphone_list in triphone_list_list:
        for triphone in triphone_list:
            total_triphone = total_triphone + 1
            if triphone in cover_status:
                cover_status[triphone] = cover_status[triphone] + 1
            else:
                cover_status[triphone] = 1
    return cover_status


def get_triphone_listlist_idfile(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    triphone_list_list = generate_lines_triphone(lines)
    return triphone_list_list

def compute_extend_cover_num(cover_status, triphone_list, doextend=False):
    extend_num = 0
    extend_cover_status = {}
    for triphone in triphone_list:
        if triphone in cover_status or triphone in extend_cover_status:
            continue
        else:
            extend_num = extend_num + 1
            extend_cover_status[triphone] = 1
    if doextend == True:
        for key, value in extend_cover_status.items():
            cover_status[key] = value
    return extend_num

#need to give high frequency word with high weight
def compute_extend_cover_score(cover_status, triphone_list, doextend=False):
    score = 0
    extend_cover_status = {}
    enough_occurtime = 5
    new_triphone_bonus = 10
    for triphone in triphone_list:
        orig_occur = 0
        extend_occur = 0
        if triphone in cover_status:
            orig_occur = cover_status[triphone]
        if triphone in extend_cover_status:
            extend_occur = extend_cover_status[triphone]

        if orig_occur + extend_occur > enough_occurtime:
            continue
        elif orig_occur == 0 and extend_occur == 0:
            score = score + new_triphone_bonus
            extend_cover_status[triphone] = 1
        else:
            extend_cover_status[triphone] = extend_occur + 1
            score = score + (enough_occurtime - orig_occur - extend_occur)

    if doextend == True:
        for key, value in extend_cover_status.items():
            cover_status[key] = value

    return score


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

def generate_lines_triphone(lines):
    triphone_list_list = []
    for line in lines:
        triphones_list = generate_line_triphone(line)
        triphone_list_list.append(triphones_list)
    return triphone_list_list

#input a line of id
#output a list of triphone
def generate_line_triphone(line):
    ids_list = line.split()
    triphones = []
    length = len(ids_list)
    for index in range(0, length):
        current_value = ids_list[index]
        if index == 0 and index == length - 1:
            pri_value = 0
            next_value = 0
        elif index == 0:
            pri_value = 0
            next_value = ids_list[index+1]
        elif index == length - 1:
            pri_value = ids_list[index-1]
            next_value = 0
        else:
            pri_value = ids_list[index-1]
            next_value = ids_list[index+1]
        #cover_str = '%d-%d-%d' % (pri_value, current_value, next_value)
        cover_str = '%s-%s-%s' % (pri_value, current_value, next_value)
        triphones.append(cover_str)
    return triphones

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
    test_extend_triphone()

