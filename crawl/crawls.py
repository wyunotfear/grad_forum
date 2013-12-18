# -*- coding: utf-8 -*-
'''
Created on 2013年12月17日

@author: User
'''
import time
import json
import crawl.items
from crawl.items import cols,forum_cols,Headline,ForumColsHeadlines
import crawl.spiders


from ini_redis import the_redis
def test_update(a_redis):
    a_redis.set('last_update',time.time())


def forum_cols_headlines_redisjson(key,forum_cols_headlines):
    '''将 ForumColsHeadlines对象持久化到redis的一个键中
    dumps->set
    '''
    def serialize_fch(fch):#fch:ForumColsHeadlines
        fch_jsonable=dict.fromkeys(fch.__dict__,[])#创建返回用的字典
        #In [149]: dd=dict.fromkeys(fch.__dict__,[])
        #In [150]: dd
        #Out[150]: 
        #{'con': [], 'eco': [], 'his': [], 'inf': [], 'int': [], 'law': [], 'let': [], 'lif': [], 'mac': [], 'man': [], 'met': [], 'nur': [], 'pha': [], 'phi': [], 'sug': [], 'wei': []}
        for col in fch_jsonable:
            if len(getattr(fch,'con'))>0:
                for headline in getattr(forum_cols_headlines,col):
                    fch_jsonable[col].append(headline.__dict__)
        return fch_jsonable
    
    the_redis.set(key,json.dumps(forum_cols_headlines,default=serialize_fch))
 
def update_forum_cols_headlines():
    forum_cols_fores=ForumColsHeadlines()#存放预告信息
    forum_cols_news=ForumColsHeadlines()#存放新闻信息
    for col in cols:
        #the_redis.delete(col)
        col_fores_spider_name=col+'_fores_spider'
        col_news_spider_name=col+'_news_spider'
        #对每个学院字母代码 反射找到对应预告和新闻的爬虫函数并执行 
        #返回时headlines实例的列表 赋值给新闻信息对象和预告信息对象中的属性
        setattr(forum_cols_fores,col,\
                getattr(crawl.spiders,col_fores_spider_name)())
        setattr(forum_cols_news,col,\
                getattr(crawl.spiders,col_news_spider_name)())
    
    #新的每个学院的新闻列表和预告列表存放在两个对象中
    #redis中只对应两个键
    the_redis.delete('forum_cols_fores')
    the_redis.delete('forum_cols_news')
    forum_cols_headlines_redisjson('forum_cols_fores',forum_cols_fores)
    forum_cols_headlines_redisjson('forum_cols_news',forum_cols_news)
    