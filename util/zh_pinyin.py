#! /usr/bin/env python2.7
#coding=utf-8
import os
from compat import u

pinyin_dict = {}
dat = os.path.join(os.path.dirname(__file__), "../data/pinyin.txt")
with open(dat) as f:
  for line in f:
    k, v = line.decode('utf-8').strip().split('\t') #这里也可转可不转!因为英文和数字不需要转？？
    #pinyin_dict[k] = v.lower().split(" ")[0][:-1]
    pinyin_dict[k] = v.lower().split(" ")[0]

def pinyin_generator(chars):
    """Generate pinyin for chars, if char is not chinese character,
    itself will be returned.
    Chars must be unicode list.
    """
    for char in chars:
      key = "%X" % ord(char)
      yield pinyin_dict.get(key, char)

def get(s, delimiter=''):
    """Return pinyin of string, the string must be unicode
    """
    return delimiter.join(pinyin_generator(u(s)))
