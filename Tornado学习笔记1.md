# Tornado 入门

tornado中文指南地址：http://demo.pythoner.com/itt2zh/

GitHub路径：git@github.com:changkuanshenhj/mServices.git

课程的GitHub地址：https://github.com/disenQF/mServices/

```shell
git init
git add .
git commit -m "first commit"
git branch -M main
git remote add origin git@github.com:changkuanshenhj/mServices.git
git push -u origin main /git push -u origin master
第一次要使用-u
移除origin
git remote remove origin
```

安装：

```python
pip install tornado==4.5 -i https://mirrors.aliyun.com/pypi/simple

```

Hello

```python
from tornado.web import Application
from tornado.ioloop import IOLoop
from tornado.web import RequestHandler


class IndexHandler(RequestHandler):
    def get(self):
        # 向客户端响应数据
        self.write('<h3>hello Tornado</h3>')


if __name__ == '__main__':
    # 创建WEB应用
    app = Application([
        ('/', IndexHandler)
    ])
    # 绑定端口
    app.listen(7000)

    # 启动Web服务
    print('starting http://localhost:%s' % 7000)
    IOLoop.current().start()
```

## 一、Tornado请求与响应

### 1.1 请求的参数如何获取

#### 1.1.1 参数的来源

+ RequestHandler对象中提供的方法来获取
+ RequestHandler对象中的request对象的字典来获取
  + request是HTTPServerRequest类对象
  + request所有的信息以字典格式存储的，且value的数据类型都是字节类型
    + arguments
    + query_arguments
    + body_arguments

####  1.1.2 读取参数的方式

​    根据不同的请求方式来获取不同的请求参数。

+ self.get_argument()/get_arguments()可以获取任何请求方式的请求参数

+ self.get_query_argument()/get_query_arguments()只获取get请求的查询参数

  ```python
  def get(self, *args, **kwargs):
      # 请求参数的读取
      # 1. 读取单个参数
      wd = self.get_argument('wd')
      print(wd)
      # 2. 读取多个参数名相同的参数值
      titles = self.get_arguments('title')
      print(titles)
  
      # 3. 从查询参数中读取url路径参数
      wd2 = self.get_query_argument('wd')
      print(wd)
      titles2 = self.get_query_arguments('title')
      print(titles2)
  
      # 4. 从请求对象中读取参数（不建议）
      req: HTTPServerRequest = self.request
      # request请求中的数据都是dict字典类型
      wd3 = req.arguments.get('wd')
      print(wd3)  # 字典key对应的value都是bytes字节类型
      wd4 = req.query_arguments.get('wd')
      print(wd4)
  ```

  

+ self.get_body_argument()/get_body_arguments() 可以获取put/post方法的表单参数

  ```python
  def post(self):
       city = self.get_body_argument('city')
       print(city)
       names = self.get_body_arguments('name')
       print(names)
       self.write('<h3>大家好,我是POST请求方法</h3>')
  def test_index_post(self):
       url = self.base_url + '/'
       # 发起post请求，表单参数使用data来指定
       resp = requests.post(url, data={
           'name': ['ck', 'cxk'],
           ‘city': '山西'
       })
       print(resp.text)
  ```

  

### 1.2 请求对象中包含哪些信息

+ 字典类型
  + arguments(query_arguments/body_arguments)
  + headers
  + cookies
  + files
+ 普通类型
  + remote_ip
  + path
  + method
  + host
  + host_name

### 1.3 Cookie和Header如何读取与设置

+ Cookie的设置和读取
  + self.get_cookie(*name*,path,domain)
  + self.set_cookie(name,path,domain)
  + self.request.cookies 获取所有的cookies
  + self.clear_cookie(name,path,domain)
+  Headerd的设置和读取
  + self.set_header(name,value)
  + self.request.headers
  + self.clear_header()

### 1.4 响应的信息如何设置

+ self.write(html)
+ self.set_status(status_code)
+ self.cookie(name, value)
+ self.set_header(name, value) 设置响应头

### 1.5 重定向

+ self.redirect('/') 重定向到新的请求

# 二、路由规则

路由则表示url，在url中可以使用正则向后端服务处理函数传入变量参数。类传于flask的path的变量

在Application的handlers中指定的路由url可以设置变量，必须是一个分组

+ 在指定方法处理函数（def get(*******)）中，必须提供接受url路径中的变量值的参数。

+ 如果url路由中存在多个变量，在方法的参数列表也应该是多个，且由左到右依次对应接受。

+ 但是，如果正则分组中声明 了分组名，则按名称传值。即分组名就是函数的参数名。

```python
return tornado.web.Application([
(r'/order/(\d+)/(\d+)', OrderHandler)
], default_host=tornado.options.options.host)
```

```python
return tornado.web.Application([
(r'/order/(?P<action_code>\d+)/(?P<order_id>\d+)', OrderHandler)
], default_host=tornado.options.options.host)
```

```python
class OrderHandler(tornado.web.RequestHandler):
    goods = [
        {
            'id': 1,
            'name': 'Python高级开发',
            'author': 'cxk',
            'price': 190
        },
        {
            'id': 2,
            'name': 'Java高级开发',
            'author': 'ck',
            'price': 290
        },
    ]
    action_map = {
        1: '取消订单',
        2: '再次购买',
        3: '评价'
    }

    def query(self, order_id):
        for item in self.goods:
            if item.get('id') == order_id:
                return item

    def get(self, order_id, action_code):
        self.write('订单查询')
        html = """
            <p>
                商品编号: %s
            </p>
            <p>
                商品名称: %s
            </p>
            <p>
                商品价格: %s
            </p>
        """
        good = self.query(int(order_id))
        self.write(html % (good.get('id'), good.get('name'), good.get('price')))
        # self.write(self.query(int(order_id)))
        self.write(self.action_map.get(int(action_code)))
```

# 三、请求切入点

说明：每次请求都会创建新的ReuqestHandler子类的对象。

1. **initialize()**

   在调用对应的行为方法(get,post)之前都会调用它（ReuqestHandler子类的对象）的initialnize()方法来进行初始化。

```python
    def initialize(self):
        # 所有的请求方法在调用之前，都会进行初始化操作
        print('-----------initialize------------')
```

2. **prepare()** 【建议选择 】

   预处理方法，在initialize()之后，行为方法之前调用的。

   主要用于验证参数、权限、读取缓存等。

3. **on_finish()**

   请求处理完成后，释放资源的方法，在行为方法完成后调用。

#  四、API接口设计

任务：通过api接口可以实现用户的登录，用户的注册，用户的信息变更和口令的修改以及用户的注销

接口：/user

1. 用户登录

   请求方法：GET

   请求参数(要求json格式)：

   | 参数名      | 类型   | 是否必选                                  |
   | ----------- | ------ | ----------------------------------------- |
   | name        | String | 必须                                      |
   | pwd         | String | 必须                                      |
   | mobile_type | int    | 可选；手机OS类型， 如android:1,ios:2,pc:3 |

   响应数据（json格式）

   ```json
   {
   	"msg": "success",
   	"token": "sgdadgajdgajdgsdf"
   }
   ```

2. 用户注册

   请求方法：POST

3. 信息变更(用户名、手机号、城市)

   请求方法：PUT

4. 修改口令

   请求方法：PUT

5. 用户注销

   请求方法：Delete

## 4.1 接受json数据

```python
class TestUserRequest(TestCase):
    url = 'http://localhost:8000/user'

    def test_login(self):
        # 上传json数据
        resp = requests.get(self.url,
                            json={
                                'name': 'cxk',
                                'pwd': '123'
                            })
        # 读取响应的json数据
        print(resp.json())
```

## 4.2 返回json数据

```python
if login_user:
    resp_data['msg'] = 'success'
    resp_data['token'] = uuid.uuid4().hex
else:
    resp_data['msg'] = '查无此用户'

self.write(resp_data)  # write()函数可接收str，dict，list
self.set_header('Content-Type', 'application/json')  # 设置响应头
```

## 4.3解决 跨域请求问题

目前跨域请求有JSAONP和CORS两种常用的方案，最广泛地使用时CORS方式。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="Referrer" content="no-referrer">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>用户登录</title>
</head>
<body>
    <button onclick="login()">登录</button>
    <div id="result"></div>
<script>
    function $(id) {
        return document.getElementById(id)
    }
    function login() {
        let req = new XMLHttpRequest();
        req.open('post', 'http://localhost:8000/user', true);
        req.setRequestHeader('Content-Type', 'application/json');
        req.onload = function (e) {
        if (req.status == 200 && req.readyState == 4){
            data = JSON.parse(req.responseText);
            $('result').innerHTML = data.msg;
        }
    };

    req.send(JSON.stringify({
        'name': 'cxk',
        'pwd': '123'
    }))
    }
</script>
</body>
</html>
```

上方使用的时Ajax请求方法

前端参考Ajax跨域请求: https://www.cnblogs.com/tkqasn/p/5869175.html

也可以使用fetch()方法

```html
<script>
    function $(id) {
        return document.getElementById(id)
    }

    function login() {
        let options = {
            method: 'post',
            body: JSON.stringify({
                'name': 'cxk',
                'pwd': '123'
            }),
            headers: {
              'Content-Type': 'application/json'
            },
            mode: 'cors'
        };
        fetch('http://localhost:8000/user', options)
            .then(response=>response.json())
            .then(data=>{
                $('result').innerHTML = data.msg;
            })

    }
</script>
```

fetch()方法的options参数中，必须有mode属性，设置为"cors"表示跨域请求。

后端代码：

```python
class LoginHandler(RequestHandler):

    users = [{
        'id': 1,
        'name': 'cxk',
        'pwd': '123',
        'last_login_device': 'Android 5.1 OnePlus5'
    }]

    def set_default_headers(self):
        # 所有的请求方法执行后，默认设置的响应头的信息
        # 以下设置响应头都是解决跨域问题
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', 'Content-Type, x-requested-with')
        self.set_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')

    def post(self):
        # 读取json数据
        bytes = self.request.body  # 字节类型
        print(bytes)
        print(self.request.headers.get('Content-Type'))

        # 从请求头中读取请求上传的数据类型（body的数据类型）
        content_type = self.request.headers.get('Content-Type')
        if content_type.startswith('application/json'):
            # self.write('upload json ok')
            json_str = bytes.decode('utf-8')
            # 反序列化为字典
            json_data = json.loads(json_str)

            resp_data = {}
            login_user = None
            # 查询用户名和口令是否正确
            for user in self.users:
                if user['name'] == json_data['name']:
                    if user['pwd'] == json_data['pwd']:
                        login_user = user
                        break
            if login_user:
                resp_data['msg'] = 'success'
                resp_data['token'] = uuid.uuid4().hex
            else:
                resp_data['msg'] = '查无此用户'

            self.write(resp_data)  # write()函数可接收str，dict，list
            self.set_header('Content-Type', 'application/json')  # 设置响应头

        else:
            self.write('upload data 必选是json格式')

    def options(self):
        # 跨域请求时，会被客户端请求，用来表示服务器是否支持跨域请求
        self.set_status(200)

    def get(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass
```

# 五、项目结构设计（拆分）

<img src="D:\Typora_files\tornado项目拆分.png" style="zoom:66%;" />

在app的init.py脚本中，创建tornado.web.Application类对象，并且设置初始化的参数

+ handlers 设置路由与请求处理类的列表
+ default_host 设置WEB服务的host名称或ip地址
+ debug 设置是否为调试模式
+ template_path 设置模板文件所在的路径
+ static_path 设置静态资源所在的目录
+ static_url_prefix 设置客户端请求静态资源的url前缀
+ ui_modules 注册UI组件，是字典类型

#  六、模板

支持jinja2的模板语言

支持的语法：

+ 填充   {{变量名}}

+ 表达式：要求表达式必须符合Python语法的规则（支持Python合肥预聚）

  + {{   1+1  }}
  + {{   "hello disen"[-5:] }}
  + {{ ','.join([str(x**2) for x in range(1, 10)]) }}

  <font color=red>注意：模板的变量不支持“点语法”，对于字典的key访问，应该是dict[key]访问</font>

+ 分支

  + {%  if条件表达式  %}    html标签   {%   end  %}
  + {%  if条件表达式  %}    html标签   {%  else %}   标签    {%   end  %}
  + {%  if条件表达式  %}    html标签  {% elif 条件%} 标签  {% else%}  标签  {%   end  %}

+ 循环

  + for循环

    ```html
    {% for val in vals %}
    	标签 {{val}}
    {% end %}
    ```

+ 支持相关的函数：

  + escape(val)

  + static_url() 生成静态资源的路径

    ```
    <link rel="stylesheet" href="{{ static_url('css/my.css') }}">
    ```

  + json_encode(val)

+ 支持“块”和替换

  + {%  block名称 %}  {%  end %}
  + {% extends "base.html" %}

+ <font color=red>支持UI组件</font>

  + 定义UI组件

    在app的包下创建ui包，将自定义UI组件类都放在ui包下。

    ```python
    from tornado.web import UIModule
    class NavModule(UIModule):
        def render(self):
            return self.render_string('ui/nav.html', menus=menus)
    ```

    注意：要在templates/ui目录下创建nav.html文件，内容如下：

    ```html
    <nav>
        <ul>
            {% for menu in menus %}
                <li>{{ menu }}</li>
            {% end %}
        </ul>
    </nav>
    ```

    因为在nav.html模板文件中使用menus变量，所以在调用此UI组件时，需要传入menus

  + 注册UI组件

    ```python
    settings = {
        'debug': True,
        'template_path': os.path.join(BASE_DIR, 'templates'),
        'static_path': os.path.join(BASE_DIR, 'static'),
        'static_url_prefix': '/s/',  # 默认是static
        'ui_modules': {
            'Nav': NavModule,
            'Menu': MenuModule
        }
    }
    ```

    在Application初始化参数中使用“ui_modules"来主持UI组件，并设置组件名称，如Nav

  + 使用UI组件

    在index.html模板中使用，内容如下：

    ```html
    {% extends 'base.html' %}
    {% block nav %}
        {% module Nav(menus) %}
    {% end %}
    ```

    {% module Nav(menus) %} 是引入组件。

# 七、数据模型ORM

## 7.1 sqlalchemy安装和MySql数据库配置

```python
pip install sqlalchemy -i https://mirrors.aliyun.com
```

关于配置pip安装源，在window系统，在用户的目录的.pip子目录中，配置pip.ini文件。

mysql数据库连接配置

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('mysql+pymysql://root:kunkun123@localhost:3306/edu?charset=utf8')

# 生成数据库连接的类
DbSession = sessionmaker(bind=engine)

# 创建会话类对象
session = DbSession()

# 生成所有模型类的父类
Base = declarative_base(bind=engine)
```

以上的code主要创建session会话连接和Base模型基类。

## 7.2 声明模型类

在app.models下创建menu.py脚本，声明Menu类

```python
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from utils.conn import Base


class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(20), unique=True, nullable=False)
    url = Column(String(50), unique=True)
    note = Column(Text)

    parent_id = Column(Integer, ForeignKey('menu.id', name='parent_id_fk'),
                       default=0, server_default='0')
    childs = relationship('Menu', backref='parent')
```

【注意】所有的模型类，必须声明"__tablename__"="menu"表名

## 7.3 创建与删除表

在pycharm工具的Pyhton console 下导入Base类，并执行创建所有模型对应的表的函数

```python
from utils.conn import Base
from app.models.menu import Menu
Base/Menu.metadata.create_all()
```

执行删除表的函数

```python
Base/Menu.metadata.drop_all()
```

## 7.4 CURD的实战

任务1：实现菜单表的CURD操作。

任务2：实现用户的管理、角色的管理、权限管理（用户、角色和菜单）

任务3：实现用户登录，不同角色的用户登录之后，所看到的菜单时不同的。

# 八、异步WEB服务

## 8.1 概念

### 8.1.1 并行与并发的概念

并行指多个任务同时在进行，一般指的是多进程（多核CPU），当然多线程也可以并行运行（受GIL全局解释器锁，同一时间点只能有一个线程在运行）。

并发指在一定的时间段内，多个任务需要同时运行，一般指的是多线程。特别是C1OK问题，解决办法是异步+消息队列。

### 8.1.2 同步与异步的概念 

同步是指调用某一任务时，要等待这个任务完成后并返回后，程序再继续向下执行。

异步是指程序调用某一任务时，不需要等待这个任务完成，程序继续向下执行。异步操作时，可以指定回调接口（函数），当任务完成后，调用回调接口回传任务完成后的数据。

### 8.1.3 协程

协程是“微线程”，不需要CPU调度，由事件循环器EventLoop（来源于IO多路复用）来监督，由用户自己调度。

Python从3.4之后，提供协程包，asyncio库，声明某一函数是协程则需要@asyncio.coroutine修饰或async标识，如果在协程中调用另一个协程则使用yield from 或 await标识。

```python
import asyncio
import requests


async def download(url):
    print('下载中%s' % url)
    await asyncio.sleep(1)
    resp = requests.get(url)
    return resp.content, resp.status_code


@asyncio.coroutine
def write_file(filename, content):
    with open(filename, 'wb') as f:
        f.write(content)
    print(filename, 'Write OK')


@asyncio.coroutine
def save(url, filename):
    print('下载中%s' % url)
    content, code = yield from download(url)
    print(url, code)
    yield from write_file(filename, content)
    print(url, filename, '保存成功')


if __name__ == '__main__':
    # 获取事件循环器对象
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait([
        save('https://www.baidu.com', 'baidu.html'),
        save('https://jd.com', 'jd.html'),
        save('https://www.mail.qq.com', 'qq_mail.html'),
    ]))

```

## 8.2 Tornado 同步和异步请求

![](D:\Typora_files\同步与异步请求（Tornado）.jpg)

### 8.2.1 发起同步请求

```python
## app--》views--》download.py
from tornado.web import RequestHandler
from tornado.httpclient import HTTPClient, HTTPResponse, HTTPRequest


class DownloadHandler(RequestHandler):
    def get(self):
        # 获取查询参数中的url（下载资源的网址）
        url = self.get_query_argument('url')
        filename = self.get_query_argument('filename', default='index.html')

        # 发起同步请求
        client = HTTPClient()
        # validate_cert 是否验证SSL安全连接的证书
        response: HTTPResponse = client.fetch(url, validate_cert=False)
        print(response.body)
        # 保存到static/downloads
        
        # 局部导包，避免循环导包
        from app import BASE_DIR, os
        dir = os.path.join(BASE_DIR, 'static/downloads')
        # encoding='utf-8' 是针对文本的
        with open(os.path.join(dir, filename), 'wb') as f:
            f.write(response.body)
        self.write('下载成功')
```

HTTPClient是HTTP请求的客户端类。

client.fetch（request）发送请求，request可以是str字符类型的URL，也可以是HTTPRequest类对象。

### 8.2.2 发起异步请求

```python
class AsyncDownloadHandler(RequestHandler):
    def save(self, response:HTTPResponse):
        # 声明回调函数，参数中必须存在response对象
        print(response.effective_url, '下载成功')
        self.write('<br>下载完成, 正在保存')
        # 在回调函数中，可以获取请求的查询参数
        filename = self.get_query_argument('filename', default='index.html')
        # 保存到static/downloads
        # 局部导包，避免循环导包
        from app import BASE_DIR, os
        dir = os.path.join(BASE_DIR, 'static/downloads')
        # encoding='utf-8' 是针对文本的
        with open(os.path.join(dir, filename), 'wb') as f:
            f.write(response.body)
        self.write('<br>保存文件成功')
        self.finish()

    @asynchronous
    def get(self):
        # 获取查询参数中的url（下载资源的网址）
        url = self.get_query_argument('url')
        filename = self.get_query_argument('filename', default='index.html')

        # 发起异步请求
        client = AsyncHTTPClient()
        # validate_cert 是否验证SSL安全连接的证书
        client.fetch(url, callback=self.save, validate_cert=False)

        self.write('下载中.......')
```

@asynchronous让请求方法变成长连接，等待finish()出现，才会关闭连接。

### 8.2.3 协程式请求

```python
class Async2DownloadHandler(RequestHandler):

    def save(self, response:HTTPResponse):
        print(response.effective_url, '下载成功')
        self.write('<br>下载完成, 正在保存')
        # 在回调函数中，可以获取请求的查询参数
        filename = self.get_query_argument('filename', default='index.html')
        # 保存到static/downloads
        # 局部导包，避免循环导包
        from app import BASE_DIR, os
        dir = os.path.join(BASE_DIR, 'static/downloads')
        # encoding='utf-8' 是针对文本的
        with open(os.path.join(dir, filename), 'wb') as f:
            f.write(response.body)
        self.write('<br>保存文件成功')
        self.finish()

    @asynchronous
    async def get(self):
        # 获取查询参数中的url（下载资源的网址）
        url = self.get_query_argument('url')
        self.write('下载中.......')
        # 同步方式发送请求，但和HTTPClient()又不一样
        client = AsyncHTTPClient()
        # validate_cert 是否验证SSL安全连接的证书
        response = await client.fetch(url, validate_cert=False)
        self.save(response)
        self.set_status(200)

    # @asynchronous
    # @gen.coroutine()
    # def get(self):
    #     # 获取查询参数中的url（下载资源的网址）
    #     url = self.get_query_argument('url')
    #     self.write('下载中.......')
    #     # 发起异步请求
    #     client = AsyncHTTPClient()
    #     # validate_cert 是否验证SSL安全连接的证书
    #     response = yield client.fetch(url, validate_cert=False)
    #     self.save(response)
    #     self.set_status(200)
```

# 九、Socket通信

## 9.1 原生的socket通信

Server服务端：

```python
import socket

# 1. 创建socket(实现网络之间的通信，还可以实现进程间的通信)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# 2. 绑定host和port端口
server.bind(('', 7000))

# 3. 监听
server.listen()

# 4. 等待接收客户端的连接
print('服务器已启动,等待连接.....')
client, address = server.accept()  # 阻塞的方法
print('%s 已连接' % address[0])
msg = client.recv(4096)
print(msg.decode('utf-8'))

# 5. 向客户端发送消息
client.send('您好，我是常小坤'.encode('utf-8'))

# 6. 等待客户端发来消息
msg = client.recv(4096)  # 阻塞方法
print(address, '说：', msg.decode())

client.close()
server.close()
```

客户端连接服务端：

```python
import socket

# 1.创建socket
socket = socket.socket()

# 2.连接服务端
socket.connect(('localhost', 7000))
socket.send('connect'.encode('utf-8'))

# 3.接收数据
msg = socket.recv(4096)  # 阻塞
print('Server：', msg.decode('utf-8'))

# 4. 向服务端发送数据
socket.send('您好，我是你的未来对象'.encode('utf-8'))

# 关闭
socket.close()
```

## 9.2 WebSocket聊天室实战

登录接口：

```python
from tornado.web import RequestHandler
class UserHandler(RequestHandler):
    def get(self):
        self.write("""
            <form method="post">
                <input name="name">
                <button>登录</button>
            </form>
        """)

    def post(self):
        name = self.get_body_argument('name')

        # 以安全的方式写入Cookie中
        self.set_secure_cookie('username', name)
        # 重定向
        self.redirect('/robbit')
```

服务端：

```python
import random
import time

from tornado.websocket import WebSocketHandler
from tornado.web import RequestHandler


class RobbitHandler(RequestHandler):
    def get(self):
        self.render('msg/robbit.html')


class MessageOlderHandler(WebSocketHandler):
    # 当前处理器是一个常链接
    def open(self):  # 表示客户请求连接
        ip = self.request.remote_ip
        # 向客户端发送消息
        self.write_message('您好！%s' % ip)

        # 每间隔一秒发送一个数字
        self.write_message('starting')
        for i in range(10):
            time.sleep(1)
            number = str(random.randint(100, 1000))
            self.write_message('%s' % number)
        self.write_message('end')


class MessageHandler(WebSocketHandler):
    # 当前处理器是一个长连接
    online_clients = []

    def send_all(self, msg):
        for client in self.online_clients:
            client.write_message(msg)

    def open(self):  # 表示客户请求连接
        # ip = self.request.remote_ip  获取当前登录的ip

        # self.online_clients.append(self)与下面的代码等价
        MessageHandler.online_clients.append(self)
        username = self.get_secure_cookie('username').decode()
        # 向客户端发送消息
        self.send_all("%s 进入聊天室" % username)

    def on_message(self, message):
        # ip = self.request.remote_ip
        username = self.get_secure_cookie('username').decode()
        msg = '%s 说: %s' % (username, message)
        self.send_all(msg)

    def on_connection_close(self):
        # self.online_clients.remove(self)
        MessageHandler.online_clients.remove(self)

```

前端robbit.html页面：

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>客服在线</title>
    <style>
        .success{
            color: green;
        }
        .error{
            color: orange;
        }
        #message_body{
            height: 200px;
            border: 1px solid lightgray;
            padding: 5px;
            background-color: cornsilk;
            overflow: scroll;
        }
    </style>
</head>
<body>
<h1>聊天室</h1>
<div id="message_body"></div>
<div>
    <input id="msg"><button>发送</button>
</div>
<script>
    function $(id) {
        return document.getElementById(id)
    }

    window.onload = function (ev) {
        var socket = new WebSocket('ws://localhost:8000/message')
        //接收服务端发送过来的信息时的回调函数
        socket.onmessage = function (ev2) {
            //console.log('-------onmessage----------');
            //console.log(ev2);
            data = ev2.data;
            $('message_body').innerHTML += '<br>' + data;
        };

        var btn = document.getElementsByTagName('button')[0];
        btn.addEventListener('click', function (e) {
            msg = $('msg').value;
            socket.send(msg); //向服务端发送数据
        })
    }
</script>
</body>
</html>
```

#  十、Tornado参考

Tornado之源码解析参考：https://blog.csdn.net/fenglei0415/article/details/84029012
