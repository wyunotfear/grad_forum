# -*- coding: utf-8 -*-
'''
Created on 2013年12月17日
定义爬取各页面的spider
一个页面一个spider
以及更新方法 更新方法在需要更新时被线程启动
@author: User
'''
import datetime
import time
import urllib
import bs4
from bs4 import BeautifulSoup
import ini_redis
from ini_redis import the_redis
from crawl.items import Headline

LATEST=3

def phi_fores_spider():
    url='http://www.sps.sdu.edu.cn/sps80/list_all.php?sortid=145'
    charset='gb2312'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req=urllib.request.Request(url,headers=headers)
    resp=urllib.request.urlopen(req)
    html_doc=(resp.read()).decode(charset)
    soup=BeautifulSoup(html_doc)
    
    headlines=[]

    def parse():
        absolute='http://www.sps.sdu.edu.cn/sps80/'
        headline_list=soup.find(id='show_news_list').ul.find_all('li')
        for li in headline_list:
            date=li.span.string
            now_st=time.localtime()#当前年月日
            now_date=datetime.date(*now_st[:3])#转换为date对象以便做差
            
            headline_date_st=time.strptime(date[1:11],'%Y-%m-%d')
            headline_date=datetime.date(*headline_date_st[:3])
            interval_d=(now_date-headline_date).days
            #显示多少天内的文章
            if interval_d<LATEST:
                title=li.a.string
                trimed_title=title if len(title)<40 else title[0:41]+'...'
                headline=Headline(href=absolute+li.a['href'],\
                                  title=title,date=li.span.string,\
                                  trimed_title=trimed_title)
                headlines.append(headline)
            else:
                break
    parse()
    
    if len(headlines)==0:
        headline=Headline(href='',\
                          title='近 '+str(LATEST)+' 天没有新信息',date='',\
                          trimed_title='近 '+str(LATEST)+' 天没有新信息')
        headlines.append(headline)          
    return headlines

def phi_news_spider():
    url='http://www.sps.sdu.edu.cn/sps80/list_all.php?sortid=146'
    charset='gb2312'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req=urllib.request.Request(url,headers=headers)
    resp=urllib.request.urlopen(req)
    html_doc=(resp.read()).decode(charset)
    soup=BeautifulSoup(html_doc)
    
    headlines=[]

    def parse():
        absolute='http://www.sps.sdu.edu.cn/sps80/'
        headline_list=soup.find(id='show_news_list').ul.find_all('li')
        for li in headline_list:
            date=li.span.string
            now_st=time.localtime()#当前年月日
            now_date=datetime.date(*now_st[:3])#转换为date对象以便做差
            
            headline_date_st=time.strptime(date[1:11],'%Y-%m-%d')
            headline_date=datetime.date(*headline_date_st[:3])
            interval_d=(now_date-headline_date).days
            #显示多少天内的文章
            if interval_d<LATEST:
                title=li.a.string
                trimed_title=title if len(title)<40 else title[0:41]+'...'
                headline=Headline(href=absolute+li.a['href'],\
                                  title=title,date=li.span.string,\
                                  trimed_title=trimed_title)
                headlines.append(headline)
            else:
                break          
    parse()
    if len(headlines)==0:
        headline=Headline(href='',\
                          title='近 '+str(LATEST)+' 天没有新信息',date='',\
                          trimed_title='近 '+str(LATEST)+' 天没有新信息')
        headlines.append(headline)                  
    return headlines

def eco_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def law_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def let_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def his_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def con_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def int_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def man_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def lif_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def inf_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def met_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def mac_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def pha_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def nur_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def sug_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def wei_fores_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]


def eco_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def law_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def let_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def his_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def con_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def int_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def man_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def lif_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def inf_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def met_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def mac_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def pha_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def nur_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def sug_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def wei_news_spider():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
    