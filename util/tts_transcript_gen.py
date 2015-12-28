#! /usr/bin/env python2.7
#coding=utf-8
#filename: tts_transcript_gen.py
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
import zh_pinyin as pinyin
import re
import random

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
            match_str = match_str.replace('"', '').replace('。', '.').replace('？', '?').replace('，', ',').replace('！', '!')
            #print match_str, len(match_str)
            if len(match_str) > 10 and len(match_str) < 30:
                converstion_lines.append(match_str)
    ftext.close()
    return converstion_lines



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

def get_average_length(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    lines = [line.decode('utf-8').strip() for line in lines]
    total_length = 0
    for line in lines:
        total_length = total_length + len(line)
    if len(lines) > 0:
        return total_length / len(lines)
    else:
        return 0



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


def triphoneid_to_phones(id2phone, triphoneid):
    ids = triphoneid.split('-')
    phones = ""
    for phoneid in ids:
        phone = id2phone.get((int(phoneid, 10)), '-')
        phones = phones + phone
    return phones

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

    if len(triphone_list) > 0:
        score = score * 1.0 / len(triphone_list)

    return score

def do_extend_cover(cover_status, triphone_list):
    for triphone in triphone_list:
        if triphone in cover_status:
            cover_status[triphone] = cover_status[triphone] + 1
        else:
            cover_status[triphone] = 1


def batch_extend_cover_status(cover_status, triphone_list_list, shuffle_ids, select_indicate, pick_batch_size):
    assert len(triphone_list_list) == len(shuffle_ids)
    assert len(shuffle_ids) == len(select_indicate)
    if pick_batch_size > len(triphone_list_list):
        print "batch size or data size is not suitble"
    random.shuffle(shuffle_ids)
    score_map = {}
    for index in range(0, len(shuffle_ids)):
        line_id = shuffle_ids[index]
        if select_indicate[line_id] == 1:
            score_map[line_id] = 0
            continue
        triphone_list = triphone_list_list[line_id]
        score = compute_extend_cover_score(cover_status, triphone_list)
        score_map[line_id] = score
    score_map = sorted(score_map.iteritems(), key=lambda d:d[1], reverse=True)
    # do extend
    current_extend_num = 0
    scan_line_num = 0
    while current_extend_num  < pick_batch_size and scan_line_num < len(shuffle_ids):
        #print "extending: ",current_extend_num, " " , scan_line_num
        line_id = score_map[scan_line_num][0]
        print line_id, score_map[scan_line_num][1]
        if select_indicate[line_id] == 0:
            #do extend
            #print "extended: ", line_id
            triphone_list = triphone_list_list[line_id]
            do_extend_cover(cover_status, triphone_list)
            select_indicate[line_id] = 1
            current_extend_num = current_extend_num + 1
        scan_line_num =  scan_line_num + 1
    return select_indicate

def sentences_extend(cover_status, triphone_list_list, pick_batch_size, batch_time):
    assert len(triphone_list_list) > pick_batch_size
    candicate_num = len(triphone_list_list)
    shuffle_ids = range(candicate_num)
    select_indicate = [0] * candicate_num
    #select_indicate = []
    #for index in xrange(candicate_num):
    #    select_indicate.append(0)
    for batch in range(batch_time):
        random.shuffle(shuffle_ids)
        print "current batch: %d %d" %(batch, len(cover_status))
        if sum(select_indicate) >= candicate_num:
            print "no enough candicate, quit"
        select_indicate = batch_extend_cover_status(cover_status, triphone_list_list, shuffle_ids, select_indicate, pick_batch_size)
    return select_indicate

def confirm_select_sentence_extend(cover_status, triphone_list_list, select_indicate):
    assert len(triphone_list_list) == len(select_indicate)
    for index in xrange(len(select_indicate)):
        if select_indicate[index] == 1:
            #print "extending index: ", index
            triphone_list = triphone_list_list[index]
            do_extend_cover(cover_status, triphone_list)

def do_extend_cover_ll(cover_status, triphone_list_list):
    for triphone_list in triphone_list_list:
        do_extend_cover(cover_status, triphone_list)

def generate_lines_triphone(lines):
    triphone_list_list = []
    for line in lines:
        triphones_list = generate_line_triphone(line)
        triphone_list_list.append(triphones_list)
    return triphone_list_list

#input a line of id
#output a list of triphone
def generate_line_triphone(line):
    if type(line) == list:
        ids_list = line
    else:
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

def extract_file_sentences(filename):
    fin = open(filename, 'r')
    lines = fin.readlines()
    fin.close()
    lines = [line.decode('utf-8').strip() for line in lines if len(line) > 0]
    split_str = []
    for line in lines:
        line = strQ2B(line)
        print "spliting ", len(line)
        if len(line) > 10:
            split_strings = line.strip().split('。')
            for ss in split_strings:
                print ss




def extend_dataset(orig_filename, extend_filename, save_filename, lexicon_filename, phoneset_filename, pick_batch_size = 10, batch_time = 20):
    lexicon_dict, phone2pinyin = read_pinyin_transcript(lexicon_filename)
    phones_dict, id2phone = read_phoneset_map(phoneset_filename)

    orig_trans_lines = convert_file_word_transcripts(orig_filename, lexicon_dict)
    orig_lines_ids = convert_transciprt_lines_ids(orig_trans_lines, phones_dict)
    orig_triphone_list_list = generate_lines_triphone(orig_lines_ids)
    cover_status = construct_triphone_count(orig_triphone_list_list)
    print_cover_status(cover_status)
    print len(cover_status)
    orig_cover_status = cover_status

    fextend = open(extend_filename, 'r')
    extend_lines = fextend.readlines()
    fextend.close()
    extend_lines = [x.decode('utf-8').strip() for x in extend_lines]
    extend_lines_ids = convert_lines_word_transcripts_id(extend_lines, lexicon_dict, phones_dict)
    extend_triphone_list_list = generate_lines_triphone(extend_lines_ids)

    select_indicate = sentences_extend(cover_status, extend_triphone_list_list, pick_batch_size, batch_time)
    print len(cover_status)
    select_sentences_id = [x for x in range(len(select_indicate)) if select_indicate[x] == 1]
    select_sentences = [extend_lines[index].decode('utf-8').strip() for index in select_sentences_id]
    fout = open(save_filename, 'w')
    for sentence in select_sentences:
        fout.write(sentence)
        fout.write('\n')
    fout.close()

def confirm_extend_dataset(orig_filename, extend_save_filename, lexicon_filename, phoneset_filename):
    lexicon_dict, phone2pinyin = read_pinyin_transcript(lexicon_filename)
    phones_dict, id2phone = read_phoneset_map(phoneset_filename)

    orig_trans_lines = convert_file_word_transcripts(orig_filename, lexicon_dict)
    orig_lines_ids = convert_transciprt_lines_ids(orig_trans_lines, phones_dict)
    orig_triphone_list_list = generate_lines_triphone(orig_lines_ids)
    cover_status = construct_triphone_count(orig_triphone_list_list)
    print_cover_status(cover_status)
    print len(cover_status)

    extend_trans_lines = convert_file_word_transcripts(extend_save_filename, lexicon_dict)
    extend_lines_ids = convert_transciprt_lines_ids(extend_trans_lines, phones_dict)
    extend_triphone_list_list = generate_lines_triphone(extend_lines_ids)
    do_extend_cover_ll(cover_status, extend_triphone_list_list)
    print len(cover_status)

