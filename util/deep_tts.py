#! /usr/bin/env python2.7
#coding=utf-8
#filename: deep_tts.py
import sys
import time
import os
import glob
import matplotlib.pyplot as plt
from os import listdir
from os.path import isfile, join
import numpy as np
from scipy.cluster.vq import whiten

from keras.models import Sequential
from keras.layers.core import Dense, Activation
from keras.layers.recurrent import LSTM


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
    np.savetxt("minval.txt", minVals, fmt="%1.8f")
    np.savetxt("ranges.txt", ranges, fmt="%1.8f")

    for textdeep_name in files:
        cmp_name = textdeep_name.replace("textdeep", "cmp_nb").replace("TextDeep", "cmp")
        save_cmp_name = cmp_name.replace("cmp_nb", "preprocess/cmp_nb")
        save_textdeep_name = textdeep_name.replace("textdeep", "preprocess/textdeep")
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

            print np.shape(text_mat), np.shape(cmp_mat)


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

def get_train_data(dirname):
    files = get_file_list(dirname)

    maxlen = 30
    X_list = []
    y_list = []
    step = 3
    for textdeep_name in files:
        cmp_name = textdeep_name.replace("textdeep", "cmp_nb").replace("TextDeep", "cmp")
        if isfile(cmp_name):
            ftext = open(textdeep_name, 'r')
            fcmp = open(cmp_name, 'r')
            text_mat = file2matrix(textdeep_name)
            cmp_mat = file2matrix(cmp_name)
            print cmp_mat[1,2] # 第一个属性对应于文件是行，第二个属性对应于列
            rows_num = np.shape(text_mat)[0]
            for i in range(0, rows_num - maxlen, step):
                X_list.append(text_mat[i:i+maxlen])
                y_list.append(cmp_mat[i:i+maxlen])

    X = np.array(X_list)
    y = np.array(y_list)

    print np.shape(X)
    print X[0, 1, 2]

    return X, y

def train(dirname):
    X_train, y_train = get_train_data(dirname)
    in_neurons = 222;
    hidden_neurons = 512;
    out_neurons = 42;
    model = Sequential()
    model.add(LSTM(output_dim=hidden_neurons, input_dim=in_neurons, return_sequences=True))
    model.add(Dense(output_dim=out_neurons, input_dim=hidden_neurons))
    model.add(Activation("linear"))
    model.compile(loss="mean_squared_error", optimizer="rmsprop")
    #json_string = model.to_json()
    #open('model_architecture.json', 'w').write(json_string)
    model.fit(X_train, y_train, batch_size=450, nb_epoch=10, validation_split=0.05)

    model.save_weights('model_weights.h5')

    #model reading
    #model = model_from_json(open('my_model_architecture.json').read())
    #model.load_weights('my_model_weights.h5')


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

def f0_statistics(dir_name, class_stat=False):
    np.set_printoptions(precision=2)
    files = get_file_list(dir_name)
    total_f0_mat = np.empty(shape=(0))
    for f0_name in files:
        if isfile(f0_name):
            fcmp = open(f0_name, 'r')
            f0_mat = file2matrix(f0_name)
            voice_indexs = (f0_mat > 1)
            f0_mat = f0_mat[voice_indexs]
            if class_stat:
                total_f0_mat = np.concatenate((total_f0_mat, f0_mat))
            else:
                max_vals = f0_mat.max()
                min_vals = f0_mat.min()
                mean_vals = f0_mat.mean()
                var_vals = f0_mat.std()
                print f0_name, " %.2f  %.2f  %.2f %.2f"  %(max_vals, min_vals, mean_vals, var_vals)
    if class_stat:
        max_val = f0_mat.max()
        min_val = f0_mat.min()
        mean_val = f0_mat.mean()
        var_val = f0_mat.std()
        #hist, bins = np.histogram(total_f0_mat, bins=50, density=True)
        #width = 0.7 * (bins[1] - bins[0])
        #center = (bins[:-1] + bins[1:]) / 2
        #plt.bar(center, hist, align='center', width=width)
        #print np.sum(hist)
        #plt.show()
        plt.hist(total_f0_mat.astype(int), 50, normed=0, facecolor='green')
        plt.xlabel('f0')
        plt.ylabel('Frequency')
        plt.title('xin150 distribute')
        plot_str = "$\mu=%.2f,\ \sigma=%.2f$" % (mean_val, var_val)
        plot_maxmin = "max=%.2f, min=%.2f" %(max_val, min_val)
        print plot_str
        #plt.text(60, .025, r'$\mu=100,\ \sigma=15$')
        plt.text(120, 100, plot_str)
        plt.text(120, 2000, plot_maxmin)
        plt.show()
        print "class_stat %2.f %2.f %.2f %.2f" %(max_val, min_val, mean_val, var_val)


if __name__ == '__main__':
    #preprocess('/Users/sooda/data/deep_tts_data/textdeep/')
    #train('/Users/sooda/data/deep_tts_data/preprocess/textdeep/')
    #f0_statistics("/Users/sooda/data/tts/labixx500/hts/data/lf0_nb/", True)
    f0_statistics("/Users/sooda/data/tts/jj_lf0/xin150/", True)
