from tornado.web import RequestHandler


class CookieHandler(RequestHandler):
    def get(self):
        # 验证参数中是否存在name?
        if self.request.arguments.get('name'):

            # 从查询参数中读取Cookie的名称
            name = self.get_query_argument('name')
            # 从cookies中获取name的对象或值
            value = self.get_cookie(name)
            self.write(value)
        else:
            # 查看所有的cookie
            cookies: dict = self.request.cookies
            html = """
                <ul> %s </ul>
            """
            lis = []
            for key in cookies:
                lis.append('<li>%s : %s </li>' % (key, self.get_cookie(key)))
            html = '显示所有的cookie' + html % ''.join(lis)
            html += """
                <form method="post">
                    <input name="delete_name" placeholder="请输入cookie的名称">
                    <button>提交</button>
                </form>
            """
            self.write(html)

    # 这里的post的请求当delete来做，目的是为了删除cookie
    def post(self):
        name = self.get_argument('delete_name')
        if self.request.cookies.get(name, None):
            # 存在的话
            self.clear_cookie(name)
            self.write('删除 %s 成功' % name)
        else:
            self.write('删除 %s 失败，不存在！！' % name)

        # 重定向操作时，不需要再调用self.write()
        self.redirect('/cookie')  # 重定向