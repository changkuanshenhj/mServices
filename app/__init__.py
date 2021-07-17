import os

from tornado.web import Application

from app.ui.menu import MenuModule
from app.ui.nav import NavModule
from app.views.index_v import IndexHandler
from app.views.search_v import SearchHandler
from app.views.cookie_v import CookieHandler
from app.views.order_v import OrderHandler
from app.views.download import DownloadHandler, AsyncDownloadHandler, Async2DownloadHandler


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # D:/python_tornado/microServer/app/__init__.py
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


def make_app(host='localhost'):
    # 注册的应用（也就是不同的访问路由）
    return Application([
        ('/', IndexHandler),
        ('/search', SearchHandler),
        ('/cookie', CookieHandler),
        ('/download', DownloadHandler),
        ('/download1', AsyncDownloadHandler),
        ('/download2', Async2DownloadHandler),
        (r'/order/(?P<action_code>\d+)/(?P<order_id>\d+)', OrderHandler)
    ], default_host=host, **settings)