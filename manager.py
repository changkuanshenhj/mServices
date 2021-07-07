from tornado.ioloop import IOLoop
import tornado.options as options
from app import make_app


if __name__ == '__main__':
    # 定义命令行参数
    options.define('port', default=8000, type=int, help='bind socket port')
    options.define('host', default='localhost', type=str, help='设置 host name')

    # manager.py --help   / manager.py --port=9000
    # 解析命令行参数
    options.parse_command_line()

    app = make_app(options.options.host)

    app.listen(options.options.port)  # 监听端口

    print('starting Web Server http://%s:%s' % (options.options.host, options.options.port))

    # 启动服务
    IOLoop.current().start()
