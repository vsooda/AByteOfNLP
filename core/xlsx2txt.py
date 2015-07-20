#! /usr/bin/env python2.7
#coding=utf-8
import textprocessing as tp

review = tp.get_excel_data("../data/review_set.xlsx", 1, 1, "data")
review_txt = open('reivew.txt', 'wb+')
for r in review:
    print r
    review_txt.write(r)
    review_txt.write('\n')

review_txt.close()

