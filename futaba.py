#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import re
import requests
from time import sleep
from bs4  import BeautifulSoup

PREFIX = 'http://dat.2chan.net/b/'
WAIT   = 1

class FutaROM:
  def __init__(self,str_url):

    self.str_url     = str_url
    self.lst_caturl = []

  def get_catalog(self):

    str_caturl  = self.str_url+'futaba.php?mode=cat&sort=1'
    o_response  = requests.get(str_caturl) 
    bs_parser   = BeautifulSoup(o_response.text, "html.parser")
    bs_catalog  = bs_parser.findAll("table", attrs={"border":"1","align":"center"})[0]
    bs_links    = bs_catalog.findAll("a", attrs={"target":"_blank"})

    for bs_link in bs_links:
      self.lst_caturl.append(PREFIX+bs_link.attrs['href'])
    return self.lst_caturl

  def get_thread(self,str_url):

    lst_id=[]
    lst_text=[]
    lst_thread=[]

    response  = requests.get(str_url)
    bs_parser = BeautifulSoup(response.text, "html.parser")
    lst_id=bs_parser.findAll("input",attrs={"type":"checkbox","value":"delete"})
    lst_text=bs_parser.findAll("blockquote")

    for i in range(len(lst_id)):
      str_id   = lst_id[i].get("name")
      str_text = lst_text[i].get_text()
      lst_thread.append((str_url,str_id,str_text))
      #print  str_url,str_id,str_text

    return lst_thread

  def get_all_thread(self):
     
    lst_all=[] 

    for str_url in self.get_catalog():
        sleep(WAIT)
        lst_all.append(self.get_thread(str_url))

    return lst_all

  def get_head(self,str_url):

    response  = requests.get(str_url)
    bs_parser = BeautifulSoup(response.text, "html.parser")
    str_id=bs_parser.find("input",attrs={"type":"checkbox","value":"delete"}).get("name")
    str_text=bs_parser.find("blockquote").get_text()

    #print  str_url,str_id,str_text
    return str_url,str_id,str_text

  def get_all_head(self):
     
    lst_all=[]

    for str_url in self.get_catalog():
        sleep(WAIT)
        lst_all.append(self.get_head(str_url))

    return lst_all

def main():

  o_futaba = FutaROM(PREFIX)

  #print o_futaba.get_catalog()
  print o_futaba.get_all_head()
  #print o_futaba.get_all_thread()
      
if __name__=='__main__':
  main()
