#! /usr/bin/env python2.7
#coding=utf-8
import sys
py2 = sys.version_info < (3, 0)

if py2:
  str_type = unicode
  #print "python 2"
  def u(s):
    if not isinstance(s, unicode):
      s = unicode(s, "utf-8")
    return s
else:
  str_type = str
  #print "python 3"
  def u(s):
    return s
