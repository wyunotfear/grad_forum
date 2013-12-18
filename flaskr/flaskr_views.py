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

from flaskr.flaskr_app import flask_app
from flask import g,render_template

from threading import Thread

import ini_redis
from ini_redis import the_redis

from crawl.crawls import *

#from celeryproj.tasks import update
#from celeryproj.celery_me import update
    
@flask_app.before_request
def to_update():
    g_redis=getattr(flask.g,'redis',None)
    if g_redis==None:
        flask.g.redis=the_redis
        g_redis=getattr(flask.g,'redis',None)
        
    def need_update():
    #先从g对象中获取redis连接
        #如果上次更新时间不存在  在当前线程中执行更新 更新完后设置更新时间 返回false
        if g_redis.get('last_update')==None:
            update_forum_cols_headlines()
            g_redis.set('last_update',time.time())
            return False
        #如果上次更新时间存在 如果比当前时间小3600 及一个小时 则执行更新
        #这里在开发阶段可以设置小些 以便查看功能执行情况
        if g_redis.get('last_update')!=None and \
        time.time()-float(g_redis.get('last_update'))>10:
            g_redis.set('last_update',time.time())
            return True
        else:
            return False
    #print(the_redis)
    #print(g_redis)
    if need_update():
        #t=Thread(target=test_update,args=(g_redis,))
        t=Thread(target=update_forum_cols_headlines)
        t.start()
        
@flask_app.route('/')
def hello_world():
    return 'Hello World!'

@flask_app.route('/testtemplate/')
def test_template():
    return render_template('basic.html')

@flask_app.route('/testredis/')
def testredis():
    return render_template('basic.html',\
                           test=flask.g.redis.get('last_update'))

@flask_app.route('/forum/')
def forum():
    

        