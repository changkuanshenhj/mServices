from tornado.web import RequestHandler
import json


class SearchHandler(RequestHandler):
    mapper = {
        'python': 'python是最流行的AI语言',
        'java': 'java 也的学啊，很厉害'
    }

    def get(self):
        html = """
            <h3>搜索%s结果</h3>
            <p>
                %s
            </p>
        """
        wd = self.get_query_argument('wd')
        result = self.mapper.get(wd)
        # self.write(html % (wd, result))
        resp_data = {
            'wd': wd,
            'result': result
        }
        # 设置响应头的数据类型
        self.set_header('Content-Type', 'application/json;charset=utf-8')
        self.write(json.dumps(resp_data))
        self.set_status(200)  # 设置响应状态码
        # cookie操作
        self.set_cookie('wd', wd)