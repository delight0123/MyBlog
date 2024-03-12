'''
通过Web框架的@get和ORM框架的Model支持，可以很容易地编写一个处理首页URL的函数


MVC是一种软件设计模式，用于组织和实现用户界面和应用程序的代码。MVC代表Model-View-Controller，其中每个组件有不同的职责：
模型、视图和控制器。
'''

import re, time, json, logging, hashlib, base64, asyncio

from coroweb import get, post

from model import User, Comment, Blog, next_id

@get('/')
async def index(request):
    users = await User.findAll()
    return {
        '__template__': 'test.html',
        'users': users
    }