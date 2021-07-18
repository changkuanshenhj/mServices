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
