#! /usr/bin/env python2.7
#coding=utf-8

"""
Compute a review's positive and negative score, their average score and standard deviation.
This module aim to extract review positive/negative score, average score and standard deviation features (all 6 features).
Sentiment analysis based on sentiment dictionary.

"""
import numpy as np
import textprocessing as tp

# 2. Sentiment dictionary analysis basic function
# Function of matching adverbs of degree and set weights
def match(word, sentiment_value):
    if word in mostdict:
        sentiment_value *= 2.0
    elif word in verydict:
        sentiment_value *= 1.5
    elif word in moredict:
        sentiment_value *= 1.25
    elif word in ishdict:
        sentiment_value *= 0.5
    elif word in insufficientdict:
        sentiment_value *= 0.25
    elif word in inversedict:
        sentiment_value *= -1
    return sentiment_value

# Function of transforming negative score to positive score
# Example: [5, -2] →  [7, 0]; [-4, 8] →  [0, 12]
def transform_to_positive_num(poscount, negcount):
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
def sumup_sentence_sentiment_score(score_list):
    score_array = np.array(score_list) # Change list to a numpy array
    Pos = np.sum(score_array[:,0]) # Compute positive score
    Neg = np.sum(score_array[:,1])
    AvgPos = np.mean(score_array[:,0]) # Compute review positive average score, average score = score/sentence number
    AvgNeg = np.mean(score_array[:,1])
    StdPos = np.std(score_array[:,0]) # Compute review positive standard deviation score
    StdNeg = np.std(score_array[:,1])

    return [Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg]

def get_single_sent_count(cuted_sents):
    single_review_senti_score = []
    for sent in cuted_sents:
        seg_sent = tp.segmentation(sent, 'list')
        i = 0 # word position counter
        a = 0 # sentiment word position
        poscount = 0 # count a positive word
        negcount = 0 # count a negative word

        #match 用于表示程度
        for word in seg_sent:
           if word in posdict:
               poscount += 1
               for w in seg_sent[a:i]:
                  poscount = match(w, poscount)
               a = i + 1

           elif word in negdict:
               negcount += 1
               for w in seg_sent[a:i]:
                negcount = match(w, negcount)
               a = i + 1

           # Match "!" in the review, every "!" has a weight of +2
           elif word == "！".decode('utf8') or word == "!".decode('utf8'):
               for w2 in seg_sent[::-1]:
                   if w2 in posdict:
                       poscount += 2
                       break
                   elif w2 in negdict:
                       negcount += 2
                       break
           i += 1

        single_review_senti_score.append(transform_to_positive_num(poscount, negcount))
    return single_review_senti_score


def single_review_sentiment_score(review):
    cuted_review = tp.cut_sentence_2(review)
    single_review_senti_score = get_single_sent_count(cuted_review)
    review_sentiment_score = sumup_sentence_sentiment_score(single_review_senti_score)
    return review_sentiment_score


# 3.2 All review dataset's sentiment score
def sentence_sentiment_score(dataset):
    dataset = dataset[1:10]
    cuted_review = []
    for cell in dataset:
        cuted_review.append(tp.cut_sentence_2(cell))
    single_review_count = []
    all_review_count = []
    for review in cuted_review:
        single_review_count = get_single_sent_count(review)
        all_review_count.append(single_review_count)
    return all_review_count


# Compute a single review's sentiment score
def all_review_sentiment_score(senti_score_list):
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
def store_sentiment_dictionary_score(review_set, storepath):
    sentiment_score = all_review_sentiment_score(sentence_sentiment_score(review_set))
    f = open(storepath,'w')
    for i in sentiment_score:
        f.write(str(i[0])+'\t'+str(i[1])+'\t'+str(i[2])+'\t'+str(i[3])+'\t'+str(i[4])+'\t'+str(i[5])+'\n')
    f.close()


if __name__ == '__main__':
    posdict = tp.get_txt_data("../data/posdict.txt","lines")
    negdict = tp.get_txt_data("../data/negdict.txt","lines")
    mostdict = tp.get_txt_data('../data/most.txt', 'lines')
    verydict = tp.get_txt_data('../data/very.txt', 'lines')
    moredict = tp.get_txt_data('../data/more.txt', 'lines')
    ishdict = tp.get_txt_data('../data/ish.txt', 'lines')
    insufficientdict = tp.get_txt_data('../data/insufficiently.txt', 'lines')
    inversedict = tp.get_txt_data('../data/inverse.txt', 'lines')
    review = tp.get_txt_data('reivew.txt', 'lines')

    print len(review)
    print single_review_sentiment_score(review[0])
    review_score = all_review_sentiment_score(sentence_sentiment_score(review))
    for index, score in enumerate(review_score):
        #print review[index], score
        print score

