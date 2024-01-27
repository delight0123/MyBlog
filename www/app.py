#设置日志的等级为 INFO，这样程序在运行时会输出 INFO 级别及以上的日志信息
import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime

from aiohttp import web

#路由处理函数，收到http GET请求时，返回一个HTML响应。
def index(request):
    return web.Response(body=b'<h1>Awesome</h1>', content_type='text/html')

"""
一个协程函数，用于初始化Web应用程序。
设置了一个路由，将 HTTP GET 请求的根路径 / 映射到 index 函数
然后创建一个服务器，开始监听 127.0.0.1:9000 地址上，
处理根路径 '/' 的 GET 请求，并返回一个HTML页面。
"""
@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop) # 创建一个web服务器实例
    app.router.add_route('GET', '/', index)# 设置路由
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)# 创建一个TCP服务器
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop() # 获取EventLoop
loop.run_until_complete(init(loop)) # 执行coroutine
loop.run_forever() #一直运行等待接受请求