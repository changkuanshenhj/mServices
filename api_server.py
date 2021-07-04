from tornado.web import Application
from tornado.web import RequestHandler
from tornado.ioloop import IOLoop
from tornado.options import options, define, parse_command_line


class LoginHandler(RequestHandler):
    def get(self):
        print('asdasdasd')
        self.write('login_get')

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


def make_app():
    return Application(
        handlers=[
            ('/login', LoginHandler),
        ],
        default_host=options.h)


if __name__ == '__main__':
    define('p', default=8000, type=int, help='绑定的port端口')
    define('h', default='localhost', type=str, help='绑定的主机ip')
    parse_command_line()  # 解释命令行参数

    app = make_app()
    app.listen(options.p)
    print('starting http://%s:%s' % (options.h, options.p))
    IOLoop.current().start()
