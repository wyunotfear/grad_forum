# -*- coding: utf-8 -*-
'''
Created on 2013年12月11日

@author: User
'''
import sys
from datetime import datetime
import time
import traceback
import flask
from threading import Thread
from flaskr.flaskr_app import flask_app
from flask import g,render_template
import ini_redis
from ini_redis import the_redis
from crawl.crawls import *
from crawl.items import cols,forum_cols,catalog_name,\
ForumColClassifiedHeadlines
#from celeryproj.tasks import update
#from celeryproj.celery_me import update

#刷新间隔 秒
UPDATEINTERVAL=5

#@flask_app.before_request
def to_update():    
    def need_update():
    #先从g对象中获取redis连接
        #如果上次更新时间不存在  在当前线程中执行更新 更新完后设置更新时间 返回false
        if the_redis.get('last_update')==None:
            update_forum_col_classified_headlines()
            the_redis.set('last_update',time.time())
            return False
        #如果上次更新时间存在 如果比当前时间小3600 及一个小时 则执行更新
        #这里在开发阶段可以设置小些 以便查看功能执行情况
        if time.time()-float(the_redis.get('last_update'))>UPDATEINTERVAL:
            the_redis.set('last_update',time.time())
            return True
        else:
            return False
    #print(the_redis)
    #print(g_redis)
    if need_update():
        #t=Thread(target=test_update,args=(g_redis,))
        t=Thread(target=update_forum_col_classified_headlines)
        t.start()
  
@flask_app.route('/update/')
def update():
    update_forum_col_classified_headlines()
    return 'update'
   
@flask_app.route('/')
def hello_world():
    return 'Hello World!'

@flask_app.route('/testtemplate/')
def test_template():
    return render_template('basic.html')

@flask_app.route('/testredis/')
def testredis():
    return render_template('basic.html',\
                           test=the_redis.get('last_update'))

@flask_app.route('/forum/')
def forum():
    to_update()
    fetched_headlines={}
    for col in cols:
    #对每个学院字母代码 反射找到对应预告和新闻的爬虫函数并执行 
    #每个爬虫返回ForumColClassifiedHeadlines实例 
    #调用实例的save方法持久化到redis中
        for catalog in forum_cols.get(col).catalogs:
                key=':'.join((col,catalog))
                try:
                    fcch=ForumColClassifiedHeadlines.retrieve(key)
                    fetched_headlines[fcch.name]=fcch.headlines
                except Exception as e:
                    print(e)
                    fetched_headlines[key]=[]
    
    return render_template('forum.htm',fetched_headlines=fetched_headlines,\
                           forum_cols=forum_cols,cols=cols,catalog_name=catalog_name)

        
