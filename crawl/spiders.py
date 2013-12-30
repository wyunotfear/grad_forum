# -*- coding: utf-8 -*-
'''
Created on 2013年12月17日
定义爬取各页面的spider
一个页面一个spider
以及更新方法 更新方法在需要更新时被线程启动
@author: User
'''
import re
import traceback
import datetime
import time
import urllib
import bs4
from bs4 import BeautifulSoup
import ini_redis
from ini_redis import the_redis
from crawl.items import Headline,ForumColClassifiedHeadlines

LATEST=100

def phi_general_parse(soup,absolute):
        headlines=[]
        #absolute='http://www.sps.sdu.edu.cn/sps80/'
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
        return headlines
def phi_fores():
    url='http://www.sps.sdu.edu.cn/sps80/list_all.php?sortid=145'
    charset='gb2312'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req=urllib.request.Request(url,headers=headers)
    resp=urllib.request.urlopen(req)
    html_doc=(resp.read()).decode(charset)
    soup=BeautifulSoup(html_doc)
    absolute='http://www.sps.sdu.edu.cn/sps80/'
    #headlines=None
    headlines=phi_general_parse(soup,absolute)
    
    if len(headlines)==0:
        headline=Headline(href='',\
                          title='近 '+str(LATEST)+'天没有新信息',date='',\
                          trimed_title='近 '+str(LATEST)+'天没有新信息')
        headlines.append(headline)          
    return ForumColClassifiedHeadlines(name='phi:fores',headlines=headlines)

def phi_news():
    url='http://www.sps.sdu.edu.cn/sps80/list_all.php?sortid=146'
    charset='gb2312'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req=urllib.request.Request(url,headers=headers)
    resp=urllib.request.urlopen(req)
    html_doc=(resp.read()).decode(charset)
    soup=BeautifulSoup(html_doc)
    absolute='http://www.sps.sdu.edu.cn/sps80/'
           
    headlines=phi_general_parse(soup,absolute)
    if len(headlines)==0:
        headline=Headline(href='',\
                          title='近 '+str(LATEST)+'天没有新信息',date='',\
                          trimed_title='近 '+str(LATEST)+'天没有新信息')
        headlines.append(headline)                  
    return ForumColClassifiedHeadlines(name='phi:news',headlines=headlines)

def eco_fores():return None
def eco_news():return None

def law_general_parse(soup,absolute):
        headlines=[]
        #absolute='http://www.sps.sdu.edu.cn/sps80/'
        cdiv=soup.find(id="div_more_news")
        headline_list=cdiv.contents
        for li in headline_list:
            #有换行字符串出现
            if type(li)==bs4.element.Tag and \
            li.find(style="float:right;")!=None:
                #print(li)
                date=li.find(style="float:right;").string
                now_st=time.localtime()#当前年月日
                now_date=datetime.date(*now_st[:3])#转换为date对象以便做差
                
                headline_date_st=time.strptime(date[1:11],'%Y-%m-%d')
                headline_date=datetime.date(*headline_date_st[:3])
                interval_d=(now_date-headline_date).days
                #显示多少天内的文章
                if interval_d<LATEST:
                    title=li.find(style="float:left").a['title']
                    trimed_title=title if len(title)<40 else title[0:41]+'...'
                    headline=Headline(href=absolute+li.a['href'],\
                  title=title,date=date,\
                  trimed_title=trimed_title)
                    headlines.append(headline)
                else:
                    break
        return headlines
def law_news():
    url='http://www.law.sdu.edu.cn/header_sbjy_index.site?isDto=1&beanName=catalogPageBean&pageIndex=1&typeCode=0508&pageSize=10'
    charset='utf-8'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req=urllib.request.Request(url,headers=headers)
    resp=urllib.request.urlopen(req)
    html_doc=(resp.read()).decode(charset)
    soup=BeautifulSoup(html_doc.strip())
    absolute='http://www.law.sdu.edu.cn'
           
    headlines=law_general_parse(soup,absolute)
    if len(headlines)==0:
        headline=Headline(href='',\
                          title='近 '+str(LATEST)+'天没有新信息',date='',\
                          trimed_title='近 '+str(LATEST)+'天没有新信息')
        headlines.append(headline)                   
    return ForumColClassifiedHeadlines(name='law:news',headlines=headlines)
def law_fores():return None

def let_general_parse(soup,absolute):
        rp=re.compile(r'\d\d\d\d-\d\d-\d\d')
        headlines=[]
        cdiv=soup.find(id='main3Col2')
        headline_list=cdiv.table.tr.find_all('tr')[1].tr.find_all('tr')
        for li in headline_list:
            #有换行字符串出现
            if type(li)==bs4.element.Tag:
                try:
                    date=rp.search(li.find_all('a')[1]['title']).group()
                    now_st=time.localtime()#当前年月日
                    now_date=datetime.date(*now_st[:3])#转换为date对象以便做差
                    
                    headline_date_st=time.strptime(date[:],'%Y-%m-%d')
                    headline_date=datetime.date(*headline_date_st[:3])
                    interval_d=(now_date-headline_date).days
                    #显示多少天内的文章
                    if interval_d<LATEST:
                        href=li.find_all('a')[1]['href']
                        title=li.find_all('a')[1].string
                        trimed_title=title if len(title)<40 else title[0:41]+'...'
                        headline=Headline(href=absolute+href,\
                      title=title,date=date,\
                      trimed_title=trimed_title)
                        headlines.append(headline)
                    else:
                        break
                except Exception as e:
                    traceback.format_exc()
        return headlines

def let_news():
    url='http://www.lit.sdu.edu.cn/Article/ShowClass.asp?ClassID=98'
    charset='gb2312'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req=urllib.request.Request(url,headers=headers)
    resp=urllib.request.urlopen(req)
    html_doc=(resp.read()).decode(charset)
    soup=BeautifulSoup(html_doc.strip())
    absolute='http://www.lit.sdu.edu.cn'
           
    headlines=let_general_parse(soup,absolute)
    if len(headlines)==0:
        headline=Headline(href='',\
                          title='近 '+str(LATEST)+'天没有新信息',date='',\
                          trimed_title='近 '+str(LATEST)+'天没有新信息')
        headlines.append(headline)                  
    return ForumColClassifiedHeadlines(name='let:news',headlines=headlines)
def let_fores():return None

def his_general_parse(soup,absolute):
        #rp=re.compile(r'\d\d\d\d-\d\d-\d\d')
        headlines=[]
        headline_list=soup.find_all('ul')[1]
        for li in headline_list:
            #有换行字符串出现
            if type(li)==bs4.element.Tag:
                try:
                    date=li.span.string
                    now_st=time.localtime()#当前年月日
                    now_date=datetime.date(*now_st[:3])#转换为date对象以便做差
                    
                    headline_date_st=time.strptime(date[:],'%Y-%m-%d')
                    headline_date=datetime.date(*headline_date_st[:3])
                    interval_d=(now_date-headline_date).days
                    #显示多少天内的文章
                    if interval_d<LATEST:
                        href= li.a['href']
                        title=li.a['title']
                        trimed_title=title if len(title)<40 else title[0:41]+'...'
                        headline=Headline(href=absolute+href,\
                      title=title,date=date,\
                      trimed_title=trimed_title)
                        headlines.append(headline)
                    else:
                        break
                except Exception as e:
                    traceback.format_exc()
        return headlines

def his_fores():
    url='http://www.history.sdu.edu.cn/new/cf/tz/'
    charset='utf-8'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req=urllib.request.Request(url,headers=headers)
    resp=urllib.request.urlopen(req)
    html_doc=(resp.read()).decode(charset)
    soup=BeautifulSoup(html_doc.strip())
    absolute='http://www.history.sdu.edu.cn/'
           
    headlines=his_general_parse(soup,absolute)
    if len(headlines)==0:
        headline=Headline(href='',\
                          title='近 '+str(LATEST)+'天没有新信息',date='',\
                          trimed_title='近 '+str(LATEST)+'天没有新信息')
        headlines.append(headline)                  
    return ForumColClassifiedHeadlines(name='his:fores',headlines=headlines)

def his_news():
    url='http://www.history.sdu.edu.cn/new/cf/jz/'
    charset='utf-8'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req=urllib.request.Request(url,headers=headers)
    resp=urllib.request.urlopen(req)
    html_doc=(resp.read()).decode(charset)
    soup=BeautifulSoup(html_doc.strip())
    absolute='http://www.history.sdu.edu.cn/'
           
    headlines=his_general_parse(soup,absolute)
    if len(headlines)==0:
        headline=Headline(href='',\
                          title='近 '+str(LATEST)+'天没有新信息',date='',\
                          trimed_title='近 '+str(LATEST)+'天没有新信息')
        headlines.append(headline)                  
    return ForumColClassifiedHeadlines(name='his:news',headlines=headlines)

def con_general_parse(soup,absolute):
        #rp=re.compile(r'\d\d\d\d-\d\d-\d\d')
        headlines=[]
        #headline_list=soup.find_all('table')[3].find_all('table')[5].\
        #find_all('tr')
        headline_list=soup.find_all('table')[3].find_all('table')[5].find_all('tr')[2:]
        for li in headline_list:
            #有换行字符串出现
            if li.a!=None:
                try: 
                    date=li.find_all('td')[2].string[0:11]
                    print(date)
                    now_st=time.localtime()#当前年月日
                    now_date=datetime.date(*now_st[:3])#转换为date对象以便做差
                    headline_date_st=time.strptime(date[:],'%Y-%m-%d')
                    headline_date=datetime.date(*headline_date_st[:3])
                    interval_d=(now_date-headline_date).days
                    print(interval_d)
                    #显示多少天内的文章
                    if interval_d<LATEST:
                        href= li.find_all('td').a['href']
                        title=li.a['title']
                        trimed_title=title if len(title)<40 else title[0:41]+'...'
                        headline=Headline(href=absolute+href,\
                      title=title,date=date,\
                      trimed_title=trimed_title)
                        headlines.append(headline)
                    else:
                        break
                except Exception as e:
                    traceback.print_exc()
                    
        return headlines

def con_news():
    url='http://www.rxgdyjy.sdu.edu.cn/article.php?classid=149'
    charset='gb2312'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = { 'User-Agent' : user_agent }
    req=urllib.request.Request(url,headers=headers)
    resp=urllib.request.urlopen(req)
    html_doc=(resp.read()).decode(charset)
    soup=BeautifulSoup(html_doc.strip())
    absolute='http://www.rxgdyjy.sdu.edu.cn/'
           
    headlines=con_general_parse(soup,absolute)
    if len(headlines)==0:
        headline=Headline(href='',\
                          title='近 '+str(LATEST)+'天没有新信息',date='',\
                          trimed_title='近 '+str(LATEST)+'天没有新信息')
        headlines.append(headline)                  
    return ForumColClassifiedHeadlines(name='con:news',headlines=headlines)

def int_fores():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def man_fores():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def lif_fores():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def inf_fores():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def met_fores():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def mac_fores():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def pha_fores():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def nur_fores():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def sug_fores():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def wei_fores():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]



def int_news():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def man_news():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def lif_news():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def inf_news():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def met_news():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def mac_news():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def pha_news():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def nur_news():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def sug_news():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
def wei_news():return [Headline(title='你好',trimed_title='你好',href='#',date='[1970-01-01]'),]
    