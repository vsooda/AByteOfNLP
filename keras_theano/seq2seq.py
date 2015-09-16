#https://raw.githubusercontent.com/simonhughes22/PythonNlpResearch/master/Experiments/CoralBleachingAnnotated/RecurrentNeuralNetwork/keras_seq2seq_test.py


from __future__ import absolute_import
from __future__ import print_function

import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Activation, RepeatVector, TimeDistributedDense
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
from keras.preprocessing.sequence import pad_sequences
#import six.moves.cPickle
import os
import cPickle as pickle

import logging
import datetime

save_dir = os.path.expanduser("~/.keras/models")

#batch model, input the origin index data, and then sample,
#then generator the np.array to calculate
def batchSeq2seq(X, Y, max_features, maxlen):
    def to_one_hot(id):
        zeros = [0] * max_features
        zeros[id] = 1
        return zeros
    batch_size = 16
    embedding_size = 32
    hidden_size = 128

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
        sampleNums = max(100, totalSampleNum / 20)
        for i in xrange(sampleNums):
            ix = indexs[i]
            X_samples.append(X[ix])
            Y_samples.append(Y[ix])
            #print(ix)

        print('sample num ', len(X_samples))

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
                print("Y   :", " ".join(map(str, map(lambda y: np.asarray(y).argmax(), y))))
                print("Pred:", " ".join(map(str, map(lambda p: np.asarray(p).argmax(), p))))
                cnt += 1

        iterations += 1
        print("Iteration:", iterations)

    print("at: " + str(datetime.datetime.now()))

def seq2seq(xs, ys, max_features, maxlen, vocab = None):
    batch_size = 16
    embedding_size = 32
    hidden_size = 512
    load_model = True

    print('Build model...')
    if load_model:
        print('Load model...')
        model = Sequential()
        model.add(Embedding(max_features, embedding_size, mask_zero=True))
        model.add(GRU(embedding_size, hidden_size))
        model.add(Dense(hidden_size, hidden_size))
        model.add(Activation('relu'))
        model.add(RepeatVector(maxlen))
        model.add(GRU(hidden_size, hidden_size, return_sequences=True))
        model.add(TimeDistributedDense(hidden_size, max_features, activation="softmax"))
        model.compile(loss='binary_crossentropy', optimizer='adam', class_mode="binary")
        model.load_weights('model.h5')
        #model = pickle.load(open(os.path.join(save_dir, 'model.pkl'), 'rb'))
    else :
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
            if p.max() > 0 and cnt < 10:
                if vocab == None:
                    print("X   :", " ".join(map(str, x)))
                    print("Y   :", " ".join(map(str, map(lambda y: np.asarray(y).argmax(), y))))
                    print("Pred:", " ".join(map(str, map(lambda p: np.asarray(p).argmax(), p))))
                else:
                    print("X   :", " ".join(map(lambda x: vocab[x], x)))
                    print("Y   :", " ".join(map(lambda y: vocab[np.asarray(y).argmax()], y)))
                    print("Pred:", " ".join(map(lambda p: vocab[np.asarray(p).argmax()], p)))
                cnt += 1

        print("Iteration:", iterations)
        if iterations % 200 == 0 :
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            #model_save_fname = 'model_%08d.pkl' %(iterations)
            model_save_fname = 'model_9w_%09d.h5' %(iterations)
            print('saving ', model_save_fname)
            #six.moves.cPickle.dump(model, open(os.path.join(save_dir, model_save_fname), "wb"))
            #pickle.dump(model, open(os.path.join(save_dir, model_save_fname), "wb"))
            model.save_weights(model_save_fname, overwrite = True)

        iterations += 1


    print("at: " + str(datetime.datetime.now()))


def simple_num_driver():
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
    xs = np.asarray(xs)
    def to_one_hot(id):
        zeros = [0] * max_features
        zeros[id] = 1
        return zeros
    ys = map(lambda x: map(to_one_hot, x), ys)
    ys = np.asarray(ys)
    print("XS Shape: ", xs.shape)
    print("YS Shape: ", ys.shape)
    seq2seq(xs, ys, max_features, maxlen)

if __name__ == '__main__':
    simple_num_driver()
