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

网页展示：

![alt text](20240411153406.png)
PS:该项目是根据廖雪峰老师的基本教程来做的，但是用的一些语法有些陈旧了，所以这个项目对我来说主要的收获是熟悉整个流程以及了解项目开发中用到的一些技术。

比如：掌握git指令； 熟悉项目环境搭建； 熟悉构造整体项目结构； 了解一些项目中常见的概念如ORM、MVC、API、URL等; 了解一些常见操作如SQL连接、前端页面、报错处理等。。。

如果是python新手，还是可以在学习文字教程的同时来顺便跟做一下这个项目的，权当熟悉项目开发流程。