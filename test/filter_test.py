#! /usr/bin/env python2.7
#coding=utf-8
#filename: filter_test.py
import sys
sys.path.append('../')
import os
import util.filter as Filter


def testSpaceFilter(contents):
    filted = Filter.spaceFiler(text)
    return filted


if __name__ == "__main__":
    text = "sdfkjl sdkfj    sfj sdfj http://www.baidu.com "
    filted = testSpaceFilter(text)
    print filted
