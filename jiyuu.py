#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
from   futaba import FutaROM
from   time   import sleep

class Jiyuu(FutaROM):

  def __init__(self,str_url,u_keyword):

    self.u_keyword  = u_keyword

    self.lst_caturl = []
    self.lst_res    = []

    self.str_url    = str_url
    self.str_tgturl = ""

  def search(self):

    lst_url    = []
    lst_head   = self.get_all_head()

    u_pattern  = u".*"+self.u_keyword+u".*"
    re_pattern = re.compile(u_pattern)

    for tup_head in lst_head:
      if re.match(re_pattern, tup_head[-1]):
        lst_url.append(tup_head[0])
      else:
        self.str_tgturl = ""
        self.lst_res    = []
    return lst_url

  def get_allres(self):

    lst_url         = self.search()
    self.str_tgturl = lst_url[0]

    if len(lst_url) == 1:
      lst_res = self.get_thread(self.str_tgturl)
    else:
      lst_res = []

    for tup_res in lst_res:
      self.lst_res.append(tup_res)
    return self.lst_res

  def get_newres(self):

    if self.str_tgturl != "":
      lst_current = self.get_thread(self.str_tgturl)
      if len(self.lst_res) < len(lst_current):
         lst_update   = lst_current[len(self.lst_res):]
         self.lst_res = lst_current
         return lst_update
      elif lst_current == []:
         self.lst_res    = []
         self.str_tgturl = self.search()[0]
      else:
         return []
    else:
      lst_update = self.get_allres()
      return lst_update
      
def main():
  
  o_jiyuu = Jiyuu("http://dat.2chan.net/b/",u"自由")

  while True:
    for i in o_jiyuu.get_newres():
      if i != []:
        print i[-1]
      else:
        print "no update"
    sleep(60)

if __name__=='__main__':
  main()
