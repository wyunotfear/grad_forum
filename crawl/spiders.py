# -*- coding: utf-8 -*-
'''
Created on 2013年12月17日
定义爬取各页面的spider
一个页面一个spider
以及更新方法 更新方法在需要更新时被线程启动
@author: User
'''
import ini_redis
from ini_redis import the_redis
import urllib

import bs4
from bs4 import BeautifulSoup
from crawl.items import Headline

def phi_fores_spider():
    url='http://www.sps.sdu.edu.cn/sps80/list_all.php?sortid=145'
    charset='gb2312'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req=urllib.request.Request(url,headers=headers)
    resp=urllib.request.urlopen(req)
    html_doc=(resp.read()).decode(charset)
    soup=BeautifulSoup(html_doc)
    
    headlines=[Headline(title='title',href='#',date='1970-01-01'),]
    def parse():
        headline=None
        headlines.append(headline)
        
    return headlines

def eco_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def law_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def let_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def his_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def con_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def int_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def man_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def lif_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def inf_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def met_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def mac_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def pha_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def nur_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def sug_fores_spider():return [Headline(title='title',href='#',date='1970-01-01'),]

def phi_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def eco_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def law_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def let_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def his_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def con_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def int_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def man_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def lif_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def inf_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def met_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def mac_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def pha_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def nur_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
def sug_news_spider():return [Headline(title='title',href='#',date='1970-01-01'),]
    