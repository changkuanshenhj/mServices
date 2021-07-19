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