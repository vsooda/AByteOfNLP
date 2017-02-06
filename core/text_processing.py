#! /usr/bin/env python2.7
#coding=utf-8

"""
Read data from excel file and txt file.
Chinese word segmentation, postagger, sentence cutting and stopwords filtering function.

"""

import xlrd
import jieba
import jieba.posseg
import csv
jieba.load_userdict('../data/review/userdict.txt') #Load user dictionary to increse segmentation accuracy


def get_excel_data(filepath, sheetnum, colnum, para):
    table = xlrd.open_workbook(filepath)
    print filepath
    print sheetnum
    sheet = table.sheets()[sheetnum-1]
    data = sheet.col_values(colnum-1)
    rownum = sheet.nrows
    if para == 'data':
        return data
    elif para == 'rownum':
        return rownum

#保存成字典
def get_csv_data(filepath, cols):
    with open(filepath) as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        #resources = []
        resources = {}
        index = 0
        for row in f_csv:
            row = [cell.decode('utf8').strip().split(' ') for cell in row]
            items = {
                'name' : row[0],
                'sentiment' : row[1],
                'type' : row[2],
                'tools' : row[3],
                'other' : row[4]
            }
            #resources[str(index)] = items
            resources[index] = items
            index = index + 1
        return resources

def get_txt_data(filepath, para):
    if para == 'lines':
        txt_file1 = open(filepath, 'r')
        txt_tmp1 = txt_file1.readlines()
        txt_tmp2 = ''.join(txt_tmp1)
        txt_tmp2 = txt_tmp2.strip() #注意strip()
        txt_data1 = txt_tmp2.decode('utf8').split('\n')
        txt_file1.close()
        return txt_data1
    elif para == 'line':
        txt_file2 = open(filepath, 'r');
        txt_tmp = txt_file2.readline()
        txt_data2 = txt_tmp.decode('utf8')
        txt_file2.close()
        return txt_data2


def segmentation(sentence, para):
    if para == 'str':
        seg_list = jieba.cut(sentence)
        seg_result = ' '.join(seg_list)
        return seg_result
    elif para == 'list':
        seg_list2 = jieba.cut(sentence)
        seg_result2 = []
        for w in seg_list2:
            seg_result2.append(w)
        return seg_result2


def postagger(sentence, para):
    if para == 'list':
        pos_data1 = jieba.posseg.cut(sentence)
        pos_list = []
        for w in pos_data1:
             pos_list.append((w.word, w.flag)) #make every word and tag as a tuple and add them to a list
        return pos_list
    elif para == 'str':
        pos_data2 = jieba.posseg.cut(sentence)
        pos_list2 = []
        for w2 in pos_data2:
            pos_list2.extend([w2.word.encode('utf8'), w2.flag])
        pos_str = ' '.join(pos_list2)
        return pos_str




""" Maybe this algorithm will have bugs in it """
def cut_sentences_1(words):
    #words = (words).decode('utf8')
    start = 0
    i = 0 #i is the position of words
    sents = []
    punt_list = ',.!?:;~，。！？：；～ '.decode('utf8') # Sentence cutting punctuations
    for word in words:
        if word in punt_list and token not in punt_list:
            sents.append(words[start:i+1])
            start = i+1
            i += 1
        else:
            i += 1
            token = list(words[start:i+2]).pop()
    # if there is no punctuations in the end of a sentence, it can still be cutted
    if start < len(words):
        sents.append(words[start:])
    return sents

""" Sentence cutting algorithm without bug, but a little difficult to explain why"""
def cut_sentence_2(words):
    #words = (words).decode('utf8')
    start = 0
    i = 0 #i is the position of words
    token = 'meaningless'
    sents = []
    punt_list = ',.!?;~，。！？；～… '.decode('utf8')
    for word in words:
        if word not in punt_list:
            i += 1
            token = list(words[start:i+2]).pop()
            #print token
        elif word in punt_list and token in punt_list:
            i += 1
            token = list(words[start:i+2]).pop()
        else:
            sents.append(words[start:i+1])
            start = i+1
            i += 1
    if start < len(words):
        sents.append(words[start:])
    return sents

def seg_fil_excel(filepath, sheetnum, colnum):
    # Read product review data from excel file and segment every review
    review_data = []
    for cell in get_excel_data(filepath, sheetnum, colnum, 'data')[0:get_excel_data(filepath, sheetnum, colnum, 'rownum')]:
        review_data.append(segmentation(cell, 'list')) # Seg every reivew

    # Read txt file contain stopwords
    stopwords = get_txt_data('../data/review/stopword.txt', 'lines')

    # Filter stopwords from reviews
    seg_fil_result = []
    for review in review_data:
        fil = [word for word in review if word not in stopwords and word != ' ']
        seg_fil_result.append(fil)
        fil = []

    # Return filtered segment reviews
    return seg_fil_result

def seg_fil_senti_excel(filepath, sheetnum, colnum):
    # Read product review data from excel file and segment every review
    review_data = []
    for cell in get_excel_data(filepath, sheetnum, colnum, 'data')[0:get_excel_data(filepath, sheetnum, colnum, 'rownum')]:
        review_data.append(segmentation(cell, 'list')) # Seg every reivew

    # Read txt file contain sentiment stopwords
    sentiment_stopwords = get_txt_data('../data/review/sentiment_stopword.txt', 'lines')

    # Filter stopwords from reviews
    seg_fil_senti_result = []
    for review in review_data:
        fil = [word for word in review if word not in sentiment_stopwords and word != ' ']
        seg_fil_senti_result.append(fil)
        fil = []

    # Return filtered segment reviews
    return seg_fil_senti_result

if __name__ == '__main__':
    review = get_excel_data("../data/review/review_set.xlsx", 1, 1, "data")
    review_txt = open('reivew.txt', 'wb+')
    for r in review:
        print r
        review_txt.write(r)
        review_txt.write('\n')

    review_txt.close()