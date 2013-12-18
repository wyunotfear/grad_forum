# -*- coding: utf-8 -*-
'''
Created on 2013年12月10日

@author: User
'''
import tornado.options
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import flaskr
from flaskr.flaskr_app import flask_app
import flaskr.flaskr_views

import sys,os
sys.path.append(os.path.abspath('.'))

tornado.options.parse_config_file("tornado_conf.py")
http_server = HTTPServer(WSGIContainer(flask_app))
http_server.listen(80)
IOLoop.instance().start()
        