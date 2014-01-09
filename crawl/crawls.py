# -*- coding: utf-8 -*-
'''
Created on 2013年12月17日

@author: User
'''
import traceback
import time
import json
import crawl.items
from crawl.items import cols,forum_cols,Headline,\
ForumColClassifiedHeadlines
import crawl.spiders
from crawl.spiders import *
from ini_redis import the_redis

def test_update(a_redis):
    a_redis.set('last_update',time.time())

def update_forum_col_classified_headlines():
    for col in cols:
        #对每个学院字母代码 反射找到对应预告和新闻的爬虫函数并执行 
        #每个爬虫返回ForumColClassifiedHeadlines实例 
        #调用实例的save方法持久化到redis中
        try:
            for catalog in forum_cols.get(col).catalogs:
                spider='_'.join((col,catalog))
                key=':'.join((col,catalog))
                fcch=getattr(crawl.spiders,spider)()
                the_redis.delete(key)
                fcch.save()
        except:
            print('error when dealing:'+col)
            traceback.print_exc()

    