#! /usr/bin/env python2.7
#coding=utf-8
#filename: deep_tts.py
import sys
import time
import os
import glob
from os import listdir
from os.path import isfile, join
import numpy as np
from scipy.cluster.vq import whiten


def get_file_list(path):
    path = os.path.abspath(path)
    files = os.listdir(path)
    for index, item in enumerate(files):
        files[index] = os.path.join(path, files[index])
    files = sorted(files)
    return files

#input the input feature dir
def preprocess(dirname):
    files = get_file_list(dirname)
    index = 0
    max_file_nums = -1
    total_cmp_mat = np.empty(shape=(0,0))

    for textdeep_name in files:
        cmp_name = textdeep_name.replace("textdeep", "cmp_nb").replace("TextDeep", "cmp")
        print cmp_name
        index = index + 1
        if index > max_file_nums and max_file_nums > 0:
            break
        if isfile(cmp_name):
            fcmp = open(cmp_name, 'r')
            cmp_mat = file2matrix(cmp_name)
            if np.shape(total_cmp_mat)[0] == 0 :
                total_cmp_mat = cmp_mat
            else:
                total_cmp_mat = np.concatenate((total_cmp_mat, cmp_mat))

    normTotal, ranges, minVals = autoNorm(total_cmp_mat)
    print ranges
    print minVals

    for textdeep_name in files:
        cmp_name = textdeep_name.replace("textdeep", "cmp_nb").replace("TextDeep", "cmp")
        save_cmp_name = cmp_name.replace("cmp_nb", "preprocess")
        save_textdeep_name = textdeep_name.replace("textdeep", "preprocess")
        index = index + 1
        if index > max_file_nums and max_file_nums > 0:
            break
        if isfile(cmp_name):
            ftext = open(textdeep_name, 'r')
            fcmp = open(cmp_name, 'r')
            text_mat = file2matrix(textdeep_name)
            cmp_mat = file2matrix(cmp_name)
            text_mat = text_mat[0:-3]
            text_num = np.shape(text_mat)[0]
            cmp_num = np.shape(cmp_mat)[0]
            if text_num < cmp_num:
                continue
            elif text_num > cmp_num:
                text_mat = text_mat[0:cmp_num]
            cmp_mat = norm_with_ranges(cmp_mat, minVals, ranges)

            np.savetxt("minval.txt", minVals, fmt="%1.8f")
            np.savetxt("ranges.txt", ranges, fmt="%1.8f")


            np.savetxt(save_cmp_name, cmp_mat, fmt='%1.8f')
            np.savetxt(save_textdeep_name, text_mat, fmt='%1.8f')

            print textdeep_name, cmp_name, save_cmp_name, save_textdeep_name


def file2matrix(filename):
    fr = open(filename)
    arrayOLines = fr.readlines()
    numberOfLines = len(arrayOLines)            #get the number of lines in the file
    length = len(arrayOLines[0].split())
    returnMat = np.zeros((numberOfLines,length))        #prepare matrix to return
    index = 0
    for line in arrayOLines:
        line = line.strip()
        listFromLine = line.split(' ')
        returnMat[index,:] = listFromLine[:]
        index += 1
    return returnMat


def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals + 1e-8
    normDataSet = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - np.tile(minVals, (m,1))
    normDataSet = normDataSet / np.tile(ranges, (m,1))   #element wise divide
    return normDataSet, ranges, minVals

def norm_with_ranges(dataSet, minVals, ranges):
    normDataSet = np.zeros(np.shape(dataSet))
    m = dataSet.shape[0]
    normDataSet = dataSet - np.tile(minVals, (m,1))
    normDataSet = normDataSet / np.tile(ranges, (m,1))   #element wise divide
    return normDataSet

if __name__ == '__main__':
    preprocess('/Users/sooda/data/deep_tts_data/textdeep/')
