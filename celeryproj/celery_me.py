'''
Created on 2013年12月11日

@author: User
'''
from __future__ import absolute_import

from celery import Celery
app = Celery('clelry_me',broker='redis://210.44.220.141:6379/0',\
             backend='redis://210.44.220.141:6379/0')
app.conf.update(
BROKER_URL = 'redis://210.44.220.141:6379/0',
CELERY_RESULT_BACKEND = 'redis://210.44.220.141:6379/0',
CELERY_TASK_SERIALIZER='json',
CELERY_ACCEPT_CONTENT=['json'], # Ignore other content
CELERY_RESULT_SERIALIZER='json'
)

import redis,time

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
        