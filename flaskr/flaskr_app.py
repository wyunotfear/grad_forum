# -*- coding: utf-8 -*-
'''
Created on 2013年12月10日

@author: User
'''
from flask import Flask,g

flask_app=Flask('flakr_app')
#redis_engin=redis.StrictRedis(host='210.44.220.141',port=6379,db=0)
#g.ini_test='ini'

if __name__=='__main__':
    flask_app.run()