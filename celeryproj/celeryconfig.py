# -*- coding: utf-8 -*-
'''
Created on 2013年12月11日

@author: User
'''
BROKER_URL = 'redis://210.44.220.141:6379/0'
CELERY_RESULT_BACKEND = 'redis://210.44.220.141:6379/0'
#CELERY_IMPORTS=["tasks"]
CELERY_TASK_SERIALIZER='json'
CELERY_ACCEPT_CONTENT=['json'] # Ignore other content
CELERY_RESULT_SERIALIZER='json'