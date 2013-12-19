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
from redis_operation.redis_om import redis_json_as_forum_cols_headlines
from crawl.items import cols,forum_cols 
#from celeryproj.tasks import update
#from celeryproj.celery_me import update

#刷新间隔 秒
UPDATEINTERVAL=5
@flask_app.before_request
def to_update():    
    def need_update():
    #先从g对象中获取redis连接
        #如果上次更新时间不存在  在当前线程中执行更新 更新完后设置更新时间 返回false
        if the_redis.get('last_update')==None:
            update_forum_cols_headlines()
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
        t=Thread(target=update_forum_cols_headlines)
        t.start()

@flask_app.route('/update/')
def update():
    update_forum_cols_headlines()
   
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
    try:
        forum_cols_fores=redis_json_as_forum_cols_headlines('forum_cols_fores')
        forum_cols_news=redis_json_as_forum_cols_headlines('forum_cols_news')
        return render_template('forum.htm',fcf=forum_cols_fores,\
                               fcn=forum_cols_news,cols=cols,forum_cols=forum_cols)
    except Exception as e:
        print(e)
        forum_cols_fores=ForumColsHeadlines()
        forum_cols_news=ForumColsHeadlines()
        return render_template('forum.htm',fcf=forum_cols_fores,\
                               fcn=forum_cols_news,cols=cols,forum_cols=forum_cols)
