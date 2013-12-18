# -*- coding: utf-8 -*-
'''
Created on 2013年12月18日

@author: User
'''
import json
import ini_redis
from ini_redis import the_redis
import crawl.items
from crawl.items import serialize_fch,ForumColsHeadlines

def forum_cols_headlines_redis_as_json(key,fch):
    '''将 ForumColsHeadlines对象持久化到redis的一个键中
    dumps->set
    '''
    the_redis.set(key,json.dumps(fch,default=serialize_fch))

def fch_hook(dic):
    fch=ForumColsHeadlines()
    return fch

def redis_json_as_forum_cols_headlines(key):
    '''forum_cols_fores键中的值(json格式)转换为ForumColsHeadlines的实例
    redisjson需要先解码为unicode才能被loads
    loads需要使用encoding=utf-8和object_hook参数
    '''
    redis_json=the_redis.get(key)
    json_s=redis_json.decode('utf-8')
    fch=json.loads(json_s,object_hook=fch_hook)
    return fch