#! /usr/bin/env python2.7
#coding=utf-8
import sys
sys.path.append('../')
#import _init_paths
'''
to predict the type of char: chinese, number, alphabet
'''

def is_chinese(uchar):
    if uchar >= u'\u4e00' and uchar<=u'\u9fa5':
        return True
    else:
        return False

def is_number(uchar):
    if uchar >= u'\u0030' and uchar<=u'\u0039':
        return True
    else:
        return False

def is_alphabet(uchar):
    if (uchar >= u'\u0041' and uchar<=u'\u005a') or (uchar >= u'\u0061' and uchar<=u'\u007a'):
        return True
    else:
        return False

def B2Q(uchar):
    '''半角转全角'''
    inside_code=ord(uchar)
    if inside_code<0x0020 or inside_code>0x7e:      #不是半角字符就返回原来的字符
        return uchar
    if inside_code==0x0020: #除了空格其他的全角半角的公式为:半角=全角-0xfee0
        inside_code=0x3000
    else:
        inside_code+=0xfee0
    return unichr(inside_code)

def Q2B(uchar):
    '''全角转半角'''
    inside_code=ord(uchar)
    if inside_code==0x3000:
        inside_code=0x0020
    else:
        inside_code-=0xfee0
    if inside_code<0x0020 or inside_code>0x7e:      #转完之后不是半角字符返回原来的字符
        return uchar
    return unichr(inside_code)

if __name__ == "__main__":
    str1 = "你是sb吗, 233？" #在代码中的字符串也是utf8格式，需要转换为unicode

    str1 = unicode(str1, "utf-8")
    #str1 = str1.decode("utf-8")
    #str2 = unicode(str1, "utf-8") #fail: decode unicode
    #str2 = str1.decode("utf-8") #可以
    for char in str1:
        print char, " " , is_chinese(char), is_number(char), is_alphabet(char), Q2B(char)
