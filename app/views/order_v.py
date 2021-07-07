from tornado.web import RequestHandler


class OrderHandler(RequestHandler):
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

    def initialize(self):
        # 所有的请求方法在调用之前，都会进行初始化操作
        print('-----------initialize------------')

    def prepare(self):
        # 初始化之后，调用行为方法之前，调用此方法进行预处理
        print('--------prepare---------')

    def post(self, order_id, action_code):
        print('----------post----------')
        self.write('------post----------')

    def get(self, order_id, action_code):
        print('----------get----------')
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

    def on_finish(self):
        print('-------on_finish-------')