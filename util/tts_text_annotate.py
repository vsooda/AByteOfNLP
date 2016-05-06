#! /usr/bin/env python2.7
#coding=utf-8
#filename: tts_transcript_gen.py
import sys
import time
import os
import glob
from os import listdir
from os.path import isfile, join
import zh_pinyin as pinyin


def alignment(text, split_pinyins):
    start_index = 0
    result_string = ""
    for pinyins in split_pinyins:
        pinyin_list = pinyins.split()
        filter(None, pinyin_list)
        length = len(pinyin_list)
        end_index = start_index + length
        if text[start_index:end_index].strip() == pinyins.strip():
            temp = pinyins
        else:
            temp = text[start_index:end_index] + " | " + pinyins
        #print text[start_index:end_index], pinyins, "--> ", temp

        if not result_string:
            result_string = temp
        else:
            result_string = result_string + " / " + temp
        start_index = end_index
    return result_string


def read_dir(dirname):
    files = get_file_list(dirname)
    index = 0
    max_file_nums = -1
    for textname in files:
        transcriptname = textname.replace("text", "transcription").replace("txt", "tr")
        index = index + 1
        if index > max_file_nums and max_file_nums > 0:
            break
        if isfile(transcriptname):
            ftext = open(textname, 'r')
            ftrans = open(transcriptname, 'r')
            text = ftext.readline().decode('utf-8').strip()
            trans = ftrans.readline().decode('utf-8').strip()
            ftext.close()
            ftrans.close()
            #for i in xrange(len(text)):
            #    print text[i]
            #print "\n"
            token_num = len(text)
            split_pinyins = trans.split("/")
            filter(None, split_pinyins) #filter the empty string in list
            pinyin_total_token = 0
            for pinyins in split_pinyins:
                pinyin_list = pinyins.split()
                filter(None, pinyin_list)
                pinyin_total_token = pinyin_total_token + len(pinyin_list)
                #print ' '.join(pinyin_list), len(pinyin_list)
            if pinyin_total_token != token_num :
                print index, textname
                print text + str(token_num) + "\n " + trans + str(pinyin_total_token)
            else:
                alignment_str = alignment(text, split_pinyins)
                output_name = textname.replace("text", "annotate")
                #print output_name, alignment_str
                fout = open(output_name, 'w')
                fout.write(alignment_str)
                fout.close()

        else:
            print transcriptname + "not found!"

def get_file_list(path):
    path = os.path.abspath(path)
    files = os.listdir(path)
    for index, item in enumerate(files):
        files[index] = os.path.join(path, files[index])
    files = sorted(files)
    return files

if __name__ == "__main__":
    read_dir("/Users/sooda/speech/speech_data/text")
    #get_file_list("../data/tts/annotate/text")
