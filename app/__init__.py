from tornado.web import Application
from app.views.index_v import IndexHandler
from app.views.search_v import SearchHandler
from app.views.cookie_v import CookieHandler
from app.views.order_v import OrderHandler


def make_app(host='localhost'):
    # 注册的应用（也就是不同的访问路径）
    return Application([
        ('/', IndexHandler),
        ('/search', SearchHandler),
        ('/cookie', CookieHandler),
        (r'/order/(?P<action_code>\d+)/(?P<order_id>\d+)', OrderHandler)
    ], default_host=host)