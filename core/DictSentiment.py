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


# 3.1 Single review's positive and negative score
# Function of calculating review's every sentence sentiment score
    def sumup_sentence_sentiment_score(self, score_list):
        score_array = np.array(score_list) # Change list to a numpy array
        Pos = np.sum(score_array[:,0]) # Compute positive score
        Neg = np.sum(score_array[:,1])
        AvgPos = np.mean(score_array[:,0]) # Compute review positive average score, average score = score/sentence number
        AvgNeg = np.mean(score_array[:,1])
        StdPos = np.std(score_array[:,0]) # Compute review positive standard deviation score
        StdNeg = np.std(score_array[:,1])
        return [Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg]

    def stopWordFilter(self, words):
        fil = [word for word in words if word not in self.stopwords and word != ' ']
        return fil

    def get_single_sent_count(self, cuted_sents):
        single_review_senti_score = []
        posdict = self.posdict
        negdict = self.negdict
        for sent in cuted_sents:
            seg_sent = tp.segmentation(sent, 'list')
            seg_sent = self.stopWordFilter(seg_sent)
            i = 0 # word position counter
            a = 0 # sentiment word position
            poscount = 0 # count a positive word
            negcount = 0 # count a negative word

            #match 用于表示程度
            for word in seg_sent:
                print '...', word
                if word in posdict:
                   poscount += 1
                   for w in seg_sent[a:i]:
                      poscount = self.match(w, poscount)
                   a = i + 1

                elif word in negdict:
                   negcount += 1
                   for w in seg_sent[a:i]:
                    negcount = self.match(w, negcount)
                   a = i + 1

                elif word == "！".decode('utf8') or word == "!".decode('utf8'):
                   for w2 in seg_sent[::-1]:
                       if w2 in posdict:
                           poscount += 2
                           break
                       elif w2 in negdict:
                           negcount += 2
                           break
                i += 1
            single_review_senti_score.append(self.transform_to_positive_num(poscount, negcount))
        return single_review_senti_score

    def single_review_sentiment_score(self, review):
        cuted_review = tp.cut_sentence_2(review)
        single_review_senti_score = self.get_single_sent_count(cuted_review)
        review_sentiment_score = self.sumup_sentence_sentiment_score(single_review_senti_score)
        return review_sentiment_score[0], review_sentiment_score[1]

# 3.2 All review dataset's sentiment score
    def sentence_sentiment_score(self, dataset):
        dataset = dataset[1:10]
        cuted_review = []
        for cell in dataset:
            cuted_review.append(tp.cut_sentence_2(cell))
        single_review_count = []
        all_review_count = []
        for review in cuted_review:
            single_review_count = self.get_single_sent_count(review)
            all_review_count.append(single_review_count)
        return all_review_count

# Compute a single review's sentiment score
    def all_review_sentiment_score(self, senti_score_list):
        score = []
        i = 0
        for review in senti_score_list:
            #print i, review
            score_array = np.array(review)
            i =  i + 1
            #import pdb
            #pdb.set_trace()
            Pos = np.sum(score_array[:,0])
            Neg = np.sum(score_array[:,1])
            AvgPos = np.mean(score_array[:,0])
            AvgNeg = np.mean(score_array[:,1])
            StdPos = np.std(score_array[:,0])
            StdNeg = np.std(score_array[:,1])
            score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])
        return score

# 4. Store sentiment dictionary features
    def store_sentiment_dictionary_score(self, review_set, storepath):
        sentiment_score = all_review_sentiment_score(sentence_sentiment_score(review_set))
        f = open(storepath,'w')
        for i in sentiment_score:
            f.write(str(i[0])+'\t'+str(i[1])+'\t'+str(i[2])+'\t'+str(i[3])+'\t'+str(i[4])+'\t'+str(i[5])+'\n')
        f.close()

if __name__ == '__main__':
    review = tp.get_txt_data('reivew.txt', 'lines')
    dict_sentiment = DictSentiment()

    print len(review)
    print dict_sentiment.single_review_sentiment_score(review[0])
    review_score = dict_sentiment.all_review_sentiment_score(dict_sentiment.sentence_sentiment_score(review))
    for index, score in enumerate(review_score):
        #print review[index], score
        print score


