#设置日志的等级为 INFO，这样程序在运行时会输出 INFO 级别及以上的日志信息
import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time
from datetime import datetime
from aiohttp import web

from jinja2 import Environment, FileSystemLoader
import orm
from coroweb import add_routes, add_static


#初始化Jinja2模板引擎，设置模板路径、自动转义等参数
def init_jinja2(app, **kw):
    logging.info('init jinja2...')
    options = dict(
        autoescape = kw.get('autoescape', True),
        block_start_string = kw.get('block_start_string', '{%'),
        block_end_string = kw.get('block_end_string', '%}'),
        variable_start_string = kw.get('variable_start_string', '{{'),
        variable_end_string = kw.get('variable_end_string', '}}'),
        auto_reload = kw.get('auto_reload', True)
    )
    path = kw.get('path', None)
    if path is None:
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
    logging.info('set jinja2 template path: %s' % path)
    env = Environment(loader=FileSystemLoader(path), **options)
    filters = kw.get('filters', None)
    if filters is not None:
        for name, f in filters.items():
            env.filters[name] = f
    app['__templating__'] = env

#日志中间件，记录每次HTTP请求的方法和路径。
async def logger_factory(app, handler):
    async def logger(request):
        logging.info('Request: %s %s' % (request.method, request.path))
        # await asyncio.sleep(0.3)
        return (await handler(request))
    return logger

#数据处理中间件，用于解析POST请求的JSON数据或表单数据
async def data_factory(app, handler):
    async def parse_data(request):
        if request.method == 'POST':
            if request.content_type.startswith('application/json'):
                request.__data__ = await request.json()
                logging.info('request json: %s' % str(request.__data__))
            elif request.content_type.startswith('application/x-www-form-urlencoded'):
                request.__data__ = await request.post()
                logging.info('request form: %s' % str(request.__data__))
        return (await handler(request))
    return parse_data

#响应处理中间件，根据处理函数的返回值不同类型，构造相应的web.Response
async def response_factory(app, handler):
    async def response(request):
        logging.info('Response handler...')
        r = await handler(request)
        if isinstance(r, web.StreamResponse):
            return r
        if isinstance(r, bytes):
            resp = web.Response(body=r)
            resp.content_type = 'application/octet-stream'
            return resp
        if isinstance(r, str):
            if r.startswith('redirect:'):
                return web.HTTPFound(r[9:])
            resp = web.Response(body=r.encode('utf-8'))
            resp.content_type = 'text/html;charset=utf-8'
            return resp
        if isinstance(r, dict):
            template = r.get('__template__')
            if template is None:
                resp = web.Response(body=json.dumps(r, ensure_ascii=False, default=lambda o: o.__dict__).encode('utf-8'))
                resp.content_type = 'application/json;charset=utf-8'
                return resp
            else:
                resp = web.Response(body=app['__templating__'].get_template(template).render(**r).encode('utf-8'))
                resp.content_type = 'text/html;charset=utf-8'
                return resp
        if isinstance(r, int) and r >= 100 and r < 600:
            return web.Response(r)
        if isinstance(r, tuple) and len(r) == 2:
            t, m = r
            if isinstance(t, int) and t >= 100 and t < 600:
                return web.Response(t, str(m))
        # default:
        resp = web.Response(body=str(r).encode('utf-8'))
        resp.content_type = 'text/plain;charset=utf-8'
        return resp
    return response

#Jinja2模板中可用的日期过滤器，用于将时间戳转换为易读的时间差或日期格式。
#在Web应用中显示相对时间，例如在评论中显示“几分钟前”、“昨天”等信息，使用户更容易理解时间的概念而无需查看具体的日期和时间
def datetime_filter(t):
    delta = int(time.time() - t)
    if delta < 60:
        return u'1分钟前'
    if delta < 3600:
        return u'%s分钟前' % (delta // 60)
    if delta < 86400:
        return u'%s小时前' % (delta // 3600)
    if delta < 604800:
        return u'%s天前' % (delta // 86400)
    dt = datetime.fromtimestamp(t)
    return u'%s年%s月%s日' % (dt.year, dt.month, dt.day)


"""
一个协程函数，用于初始化Web应用程序。

在这个协程函数中，首先使用orm.create_pool创建数据库连接池，然后初始化web.Application实例。
添加了日志和响应处理的中间件，初始化Jinja2模板引擎，设置路由和静态资源。
最后，通过loop.create_server创建服务器并启动
"""

async def init(loop):
    await orm.create_pool(loop=loop, host='localhost', port=3306, user='root', password='1234', db='awesome')
    app = web.Application(loop=loop,middlewares=[
        logger_factory, response_factory
    ])
    init_jinja2(app, filters=dict(datetime=datetime_filter))
    add_routes(app, 'urlHandlers')
    add_static(app)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    await site.start()
    # srv = await loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    # logging.info('server started at http://127.0.0.1:9000...')
    # return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()