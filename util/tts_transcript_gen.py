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

def filter_quotation(string):
    if string.startswith('“') and string.endswith('”'):
        string = string[1:-1]
    return string



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
    index = 0
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
            trans = trans + lexicon_dict.get(py, '_') + " "
    trans = trans.replace('_ _ _', '_')
    trans = trans.replace('_ _', '_')
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

def convert_lines_pinyin(lines):
    pinyin_lines = []
    for line in lines:
        line = line.decode('utf-8').strip()
        if len(line) == 0:
            print "empty line"
        else:
            han_pinyin = pinyin.get(line, ' ')
        #print line, han_pinyin


def convert_file_pinyin(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    pinyin_lines = convert_lines_pinyin(lines)
    return pinyin_lines

def is_zero_consonant(string):
    if string.startswith("a") or string.startswith("e") or string.startswith("o"):
        return True
    else:
        return False

# a o e
def is_modal(string):
    substring = string[:-1]
    if substring == 'a' or substring == 'o' or substring == 'e' :
        #print string, " is modal"
        return True
    else:
        return False

def extract_zero_consonant(filename):
    f = open(filename, 'r')
    lines = f.readlines()
    f.close()
    lines = filter_punct(lines)
    for line in lines:
        line = line.decode('utf-8').strip()
        han_pinyin = pinyin.get(line, ' ')
        if is_zero_consonant(han_pinyin):
            print line
        #pinyins = han_pinyin.split(" ")
        #count = 0
        #flag = 1
        #for py_str in pinyins:
        #    #if is_zero_consonant(py_str):
        #    if flag == 1:
        #        flag = 0
        #        if is_modal(py_str):
        #            count = count + 1
        #    if py_str == ',':
        #        #print "biao dian........"
        #        flag = 1

        #if count > 0:
        #    print line



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
        #if index == 0:
        #    print index, phone
        ids.append(index)
    return ids

def convert_transciprt_lines_ids(trans_lines, phones_dict):
    lines_ids = []
    for line in trans_lines:
        ids = convert_transcript_id(line, phones_dict)
        lines_ids.append(ids)
    return lines_ids

def covert_status2phone_counter(cover_status):
    phones_counter = {}
    for key, value in cover_status.iteritems():
        phones = key.split("-")
        current_phone = phones[1]
        if current_phone in phones_counter:
            phones_counter[current_phone] = phones_counter[current_phone] + value
        else:
            phones_counter[current_phone] = value
    return phones_counter

def print_cover_status(cover_status, id2phone=None, phone2pinyin=None):
    phones_counter = covert_status2phone_counter(cover_status)
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
    total_num = len(cover_status)
    no_one_index = len(cover_status)
    index = 0
    for key, value in cover_status:
        if value == 1:
            no_one_index = index
            break
        index = index + 1
    one_nums = total_num - no_one_index
    print one_nums , ' / ', total_num

    counter = sorted(phones_counter.iteritems(), key=lambda d:d[1], reverse=True)
    for key, value in counter:
        if id2phone:
            key = id2phone.get((int(key, 10)), '_')
        print key, value




def triphoneid_to_phones(id2phone, triphoneid):
    ids = triphoneid.split('-')
    phones = ""
    for phoneid in ids:
        phone = id2phone.get((int(phoneid, 10)), '_')
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
def compute_extend_cover_score(cover_status, triphone_list, doextend=False, phones_counter=None):
    score = 0
    extend_cover_status = {}
    enough_occurtime = 10
    new_triphone_bonus = 10
    count_punct = 0
    enough_phone_occur = 20

    for triphone in triphone_list:
        phones = triphone.split("-")
        current_phone = phones[1]
        if phones_counter:
            if current_phone in phones_counter:
                if phones_counter[current_phone] < enough_phone_occur:
                    score = score + enough_phone_occur - phones_counter[current_phone]
                    #print "add score for Seldom phone: ", current_phone, enough_phone_occur-phones_counter[current_phone]
            else:
                score = score + enough_phone_occur
                #print "add score for Seldom phone: ", current_phone, enough_phone_occur
        if current_phone == '0':
            count_punct = count_punct + 1
        escape_current_triphone = False
        for phone in phones:
            if phone == '0':
                escape_current_triphone = True
        if escape_current_triphone :
            #print "escaping: ", triphone
            continue;
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
    if count_punct > 5:
        score = score * 0.5;
    elif count_punct > 3:
        #print "punct count: ", count_punct
        score = score * 0.8;

    return score

def do_extend_cover(cover_status, triphone_list):
    for triphone in triphone_list:
        if triphone in cover_status:
            cover_status[triphone] = cover_status[triphone] + 1
        else:
            cover_status[triphone] = 1


def batch_extend_cover_status(cover_status, triphone_list_list, shuffle_ids, select_indicate, pick_batch_size, select_id_sequence):
    assert len(triphone_list_list) == len(shuffle_ids)
    assert len(shuffle_ids) == len(select_indicate)
    if pick_batch_size > len(triphone_list_list):
        print "batch size or data size is not suitble"
    random.shuffle(shuffle_ids)
    score_map = {}
    phones_counter = covert_status2phone_counter(cover_status)
    for index in range(0, len(shuffle_ids)):
        line_id = shuffle_ids[index]
        if select_indicate[line_id] == 1:
            score_map[line_id] = 0
            continue
        triphone_list = triphone_list_list[line_id]
        score = compute_extend_cover_score(cover_status, triphone_list, False, phones_counter)
        score_map[line_id] = score
    score_map = sorted(score_map.iteritems(), key=lambda d:d[1], reverse=True)
    # do extend
    current_extend_num = 0
    scan_line_num = 0
    id_sequence = []
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
            id_sequence.append(line_id)
        scan_line_num =  scan_line_num + 1
    # + 和 append 的区别
    #select_id_sequence = select_id_sequence + id_sequence #使用+， 在函数外，值被清空
    for index in id_sequence: #使用append达到预期
        select_id_sequence.append(index)
    print select_id_sequence
    return select_indicate

def sentences_extend(cover_status, triphone_list_list, pick_batch_size, batch_time, select_id_sequence, id2phone=None):
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
        select_indicate = batch_extend_cover_status(cover_status, triphone_list_list, shuffle_ids, select_indicate, pick_batch_size, select_id_sequence)
        print_cover_status(cover_status, id2phone)
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


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)

def split_with_dilimite(lines, delimite):
    sentences = []
    for line in lines:
        #print "spliting ", len(line)
        if len(line) > 10:
            find_results = list(find_all(line, delimite))
            start = 0
            substrings = []
            for index in find_results:
                substrings.append(line[start:index+1])
                start = index + 1
            if start < len(line):
                substrings.append(line[start:len(line)])
            sentences = sentences + substrings
    return sentences


def extract_file_sentences(filename):
    fin = open(filename, 'r')
    lines = fin.readlines()
    fin.close()
    lines = [line.decode('utf-8').strip() for line in lines if len(line) > 0]
    lines = [strQ2B(line) for line in lines]
    period_delimite = '。'.decode('utf-8')
    exclamation_delimite = '！'.decode('utf-8')
    interrogation_delimite = '？'.decode('utf-8')
    en_exc_delimite = "!".decode('utf-8')
    en_inter_delimite = "?".decode('utf-8')
    sentences = split_with_dilimite(lines, period_delimite)
    sentences = split_with_dilimite(sentences, exclamation_delimite)
    sentences = split_with_dilimite(sentences, interrogation_delimite)
    sentences = split_with_dilimite(sentences, en_exc_delimite)
    sentences = split_with_dilimite(sentences, en_inter_delimite)
    return sentences

def write_lines_file(filename, lines):
    fout = open(filename, 'w')
    for line in lines:
        fout.write(line)
        fout.write('\n')
    fout.close()


def filter_double_quotation(lines):
    dialogPattern = re.compile(r'".*?"');
    filter_lines = []
    for line in lines:
        line = line.decode('utf-8').strip().replace('“', '"').replace('”', '"').replace("‘", "").replace("’", "")
        line = line.replace(' ', '')
        match = dialogPattern.match(line)
        if match:
            match_str = match.group()
            if len(match_str) > 10 and len(match_str) < 30:
                filter_lines.append(match_str[1:-1])
        else:
            filter_lines.append(line)
    return filter_lines

def filter_punct(lines):
    filter_lines = []
    for line in lines:
        line = line.decode('utf-8').strip().replace('“', '').replace('”', '').replace("‘", "").replace("’", "").replace('"', '').replace('……', ',').replace(' ', '')
        no_chinese_count = 0
        for w in line:
            unicode_value = ord(w)
            if unicode_value < 19968 or unicode_value > 40869:
                no_chinese_count = no_chinese_count + 1
        #if no_chinese_count > 7:
        #    print line, no_chinese_count
        if len(line) > 32 and len(line) < 50 and no_chinese_count < 7:
            filter_lines.append(line)
    return filter_lines



def extend_dataset(orig_filename, extend_filename, save_filename, lexicon_filename, phoneset_filename, pick_batch_size = 10, batch_time = 20):
    lexicon_dict, phone2pinyin = read_pinyin_transcript(lexicon_filename)
    phones_dict, id2phone = read_phoneset_map(phoneset_filename)

    orig_trans_lines = convert_file_word_transcripts(orig_filename, lexicon_dict)
    orig_lines_ids = convert_transciprt_lines_ids(orig_trans_lines, phones_dict)
    orig_triphone_list_list = generate_lines_triphone(orig_lines_ids)
    cover_status = construct_triphone_count(orig_triphone_list_list)
    print_cover_status(cover_status, id2phone)
    print len(cover_status)
    orig_cover_status = cover_status

    fextend = open(extend_filename, 'r')
    extend_lines = fextend.readlines()
    fextend.close()
    extend_lines = [x.decode('utf-8').strip() for x in extend_lines]
    extend_lines_ids = convert_lines_word_transcripts_id(extend_lines, lexicon_dict, phones_dict)
    extend_triphone_list_list = generate_lines_triphone(extend_lines_ids)

    select_id_sequence = []
    select_indicate = sentences_extend(cover_status, extend_triphone_list_list, pick_batch_size, batch_time, select_id_sequence, id2phone)
    print len(cover_status)
    print_cover_status(cover_status)
    print select_id_sequence
    select_sentences_id = [x for x in range(len(select_indicate)) if select_indicate[x] == 1]
    select_sentences = [extend_lines[index].decode('utf-8').strip() for index in select_sentences_id]
    #select_sentences = [filter_quotation(line) for line in select_sentences]

    write_lines_file(save_filename, select_sentences)
    #fout = open(save_filename, 'w')
    #for sentence in select_sentences:
    #    fout.write(sentence)
    #    fout.write('\n')
    #fout.close()

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

