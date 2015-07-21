#! /usr/bin/env python2.7
#coding=utf-8
#filename: DictSentiment.py

import numpy as np
import textprocessing as tp

class DictSentiment:
    def __init__(self):
        self.posdict = tp.get_txt_data("../data/posdict.txt","lines")
        self.negdict = tp.get_txt_data("../data/negdict.txt","lines")
        self.mostdict = tp.get_txt_data('../data/most.txt', 'lines')
        self.verydict = tp.get_txt_data('../data/very.txt', 'lines')
        self.moredict = tp.get_txt_data('../data/more.txt', 'lines')
        self.ishdict = tp.get_txt_data('../data/ish.txt', 'lines')
        self.insufficientdict = tp.get_txt_data('../data/insufficiently.txt', 'lines')
        self.inversedict = tp.get_txt_data('../data/inverse.txt', 'lines')
        self.stopwords = tp.get_txt_data('../data/sentiment_stopword.txt', 'lines')


    def match(self, word, sentiment_value):
        if word in self.mostdict:
            sentiment_value *= 2.0
        elif word in self.verydict:
            sentiment_value *= 1.5
        elif word in self.moredict:
            sentiment_value *= 1.25
        elif word in self.ishdict:
            sentiment_value *= 0.5
        elif word in self.insufficientdict:
            sentiment_value *= 0.25
        elif word in self.inversedict:
            sentiment_value *= -1
        return sentiment_value

# Function of transforming negative score to positive score
# Example: [5, -2] →  [7, 0]; [-4, 8] →  [0, 12]
    def transform_to_positive_num(self, poscount, negcount):
        pos_count = 0
        neg_count = 0
        if poscount < 0 and negcount >= 0:
            neg_count += negcount - poscount
            pos_count = 0
        elif negcount < 0 and poscount >= 0:
            pos_count = poscount - negcount
            neg_count = 0
        elif poscount < 0 and negcount < 0:
            neg_count = -poscount
            pos_count = -negcount
        else:
            pos_count = poscount
            neg_count = negcount
        return [pos_count, neg_count]

    def stopWordFilter(self, words):
        fil = [word for word in words if word not in self.stopwords and word != ' ']
        return fil

    def cut_sentences_words(self, review):
        sent_words = []
        cuted_review = tp.cut_sentence_2(review)
        for sent in cuted_review:
            seg_sent = tp.segmentation(sent, 'list')
            seg_sent = self.stopWordFilter(seg_sent)
            sent_words.append(seg_sent)
        return sent_words


    def get_single_sent_count(self, sentences_words):
        single_review_senti_score = []
        posdict = self.posdict
        negdict = self.negdict
        for words in sentences_words:
            i = 0 # word position counter
            a = 0 # sentiment word position
            poscount = 0 # count a positive word
            negcount = 0 # count a negative word

            #match 用于表示程度
            for word in words:
                #print '...', word
                if word in posdict:
                   poscount += 1
                   for w in words[a:i]:
                      poscount = self.match(w, poscount)
                   a = i + 1

                elif word in negdict:
                   negcount += 1
                   for w in words[a:i]:
                    negcount = self.match(w, negcount)
                   a = i + 1

                elif word == "！".decode('utf8') or word == "!".decode('utf8'):
                   for w2 in words[::-1]:
                       if w2 in posdict:
                           poscount += 2
                           break
                       elif w2 in negdict:
                           negcount += 2
                           break
                i += 1
            single_review_senti_score.append(self.transform_to_positive_num(poscount, negcount))
        score_array = np.array(single_review_senti_score)
        pos_score = np.sum(score_array[:, 0])
        neg_score = np.sum(score_array[:, 1])
        return [pos_score, neg_score]

    def single_review_sentiment_score(self, review):
        sentences_words = self.cut_sentences_words(review)
        scores = self.get_single_sent_count(sentences_words)
        return scores[0], scores[1]

    def sentence_sentiment_score(self, dataset):
        dataset = dataset[1:10]
        for review in dataset:
            scores = self.single_review_sentiment_score(review)
            print scores[0], scores[1]

if __name__ == '__main__':
    review = tp.get_txt_data('reivew.txt', 'lines')
    dict_sentiment = DictSentiment()

    print len(review)
    print dict_sentiment.single_review_sentiment_score(review[0])
    dict_sentiment.sentence_sentiment_score(review)


