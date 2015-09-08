#https://raw.githubusercontent.com/simonhughes22/PythonNlpResearch/master/Experiments/CoralBleachingAnnotated/RecurrentNeuralNetwork/keras_seq2seq_test.py

'''
input: vocab, postIndex, commentIndex
'''

from __future__ import absolute_import
from __future__ import print_function

import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation, RepeatVector, TimeDistributedDense
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU

import logging
import datetime


#all return with list format
def readDataFile(vocabName, postIndexName, commentIndexName):
    fvocab = open(vocab, 'r')
    vocabLines = fvocab.readlines()
    vocab = []
    for w in vocabLines:
        w = w.strip()
        vocab.append(w)

    fpostIndex = open(postIndexName, 'r')
    postIndexLines = fpostIndex.readlines()
    postIndexs = []
    for lines in postIndexs:
        lines = lines.strip()
        indexs = lines.split(' ')

    commentIndexs = []
    return vacab, postIndex, commentIndex

#batch model, input the origin index data, and then sample,
#then generator the np.array to calculate
def batchSeq2seq(X, Y, max_features, maxlen):
    def to_one_hot(id):
        zeros = [0] * max_features
        zeros[id] = 1
        return zeros
    batch_size = 16
    embedding_size = 32
    hidden_size = 512

    print('Build model...')
    model = Sequential()
    model.add(Embedding(max_features, embedding_size, mask_zero=True))
    model.add(GRU(embedding_size, hidden_size))
    model.add(Dense(hidden_size, hidden_size))
    model.add(Activation('relu'))
    model.add(RepeatVector(maxlen))
    model.add(GRU(hidden_size, hidden_size, return_sequences=True))
    model.add(TimeDistributedDense(hidden_size, max_features, activation="softmax"))

    model.compile(loss='binary_crossentropy', optimizer='adam', class_mode="binary")

    print("Train...")
    #X_train, y_train = xs, ys

    totalSampleNum = len(X)
    indexs = range(totalSampleNum)

    iterations = 0
    while True:
        np.random.shuffle(indexs)
        X_samples = []
        Y_samples = []
        sampleNums = 10
        for i in xrange(sampleNums):
            ix = indexs[i]
            X_samples.append(X[ix])
            Y_samples.append(Y[ix])
            print(ix)

        xs = np.asarray(X_samples)
        Y_samples = map(lambda x:map(to_one_hot, x), Y_samples)
        ys = np.asarray(Y_samples)
        X_train, y_train = xs, ys
        print("XS sample Shape: ", X_train.shape)
        print("YS sample Shape: ", y_train.shape)
        results = model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=1, validation_split=0.0, show_accuracy=True, verbose=1)
        preds = model.predict_proba(X_train, batch_size=batch_size)

        cnt = 0
        for x, y, p in zip(X_train, y_train, preds):
            if p.max() > 0 and cnt < 5:
                print("X   :", " ".join(map(str, x)))
                print("Y   :", " ".join(map(str, map(lambda y: max(y), y))))
                print("Pred:", " ".join(map(str, map(lambda p: np.asarray(p).argmax(), p))))
                cnt += 1

        iterations += 1
        print("Iteration:", iterations)

    print("at: " + str(datetime.datetime.now()))

def seq2seq(xs, ys, max_features, maxlen):
    batch_size = 16
    embedding_size = 32
    hidden_size = 512

    print('Build model...')
    model = Sequential()
    model.add(Embedding(max_features, embedding_size, mask_zero=True))
    model.add(GRU(embedding_size, hidden_size))
    model.add(Dense(hidden_size, hidden_size))
    model.add(Activation('relu'))
    model.add(RepeatVector(maxlen))
    model.add(GRU(hidden_size, hidden_size, return_sequences=True))
    model.add(TimeDistributedDense(hidden_size, max_features, activation="softmax"))

    model.compile(loss='binary_crossentropy', optimizer='adam', class_mode="binary")

    print("Train...")
    X_train, y_train = xs, ys

    iterations = 0
    while True:
        results = model.fit(X_train, y_train, batch_size=batch_size, nb_epoch=1, validation_split=0.0, show_accuracy=True, verbose=1)
        preds = model.predict_proba(X_train, batch_size=batch_size)

        cnt = 0
        for x, y, p in zip(X_train, y_train, preds):
            if p.max() > 0 and cnt < 5:
                print("X   :", " ".join(map(str, x)))
                print("Y   :", " ".join(map(str, map(lambda y: max(y), y))))
                print("Pred:", " ".join(map(str, map(lambda p: np.asarray(p).argmax(), p))))
                cnt += 1

        iterations += 1
        print("Iteration:", iterations)

    print("at: " + str(datetime.datetime.now()))


def seq_test(xs, ys, max_features, maxlen):
    def to_one_hot(id):
        zeros = [0] * max_features
        zeros[id] = 1
        return zeros
    xs = np.asarray(xs)
    ys = map(lambda x: map(to_one_hot, x), ys)
    ys = np.asarray(ys)
    print("XS Shape: ", xs.shape)
    print("YS Shape: ", ys.shape)
    seq2seq(xs, ys, max_features, maxlen)

def seq_batch_test(X, Y, max_features, maxlen):
    batchSeq2seq(X, Y, max_features, maxlen)

if __name__ == '__main__':
    print("Started at: " + str(datetime.datetime.now()))
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
    logger = logging.getLogger()

    xs = []
    maxlen = 100
    max_features=maxlen + 1
    from numpy.random import shuffle
    r = range(1, maxlen + 1, 1)
    for i in range(1000):
        shuffle(r)
        new_x = r[::]
        xs.append(new_x)
    ys = xs
    #seq_test(xs, ys, max_features, maxlen)
    seq_batch_test(xs, ys, max_features, maxlen)



