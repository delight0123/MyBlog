# MyBlog
A simple blog site
参考廖雪峰老师python教程实战https://www.liaoxuefeng.com/

首先确保安装python以及MySQL,其次需要的第三方库有：

aiohttp-----(编写异步 HTTP 客户端和服务器)

jinja2-----(在Web开发中用于将数据渲染到HTML页面上，以便动态生成页面内容。常见的Web框架如Flask和Django中都有对jinja2的集成)

aiomysql-----(用于在异步应用程序中操作 MySQL 数据库)

项目目录结构如下：

backup/            ------- 备份目录

conf/              ------- 配置文件

dist/              ------- 打包目录

www/               ------- Web目录，存放.py文件

  +- static/       ------- 存放静态文件
  
  +- templates/    ------- 存放模板文件

ios/               ------- 存放iOS App工程