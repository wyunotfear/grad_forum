# -*- coding: utf-8 -*-
'''
Created on 2013年12月11日

@author: User
'''
from __future__ import absolute_import
import time
import sys,os
sys.path.append('''E:\workspace\python\grad_forum\celeryproj''')

from celery_me import app
import redis

the_redis=redis.StrictRedis(host='210.44.220.141',port=6379,db=0)
@app.task
def add(x,y):
    return x+y

@app.task
def printr():
    print('printr')
    
@app.task
def crawl():
    pass

@app.task
def update():
    the_redis.set('last_update',time.time())