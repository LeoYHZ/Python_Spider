import socket as sk
# 导入包socket，别名取为sk

def service_for_client(client):
    """处理客户端请求的"""
    print("I'm service_for_client.")
    # 接收request
    request = client.recv(1024)
    # 返回response
    # 响应行+响应头+空行+响应体
    response = "HTTP/1.1 200 OK\r\n"
    response += "Server: myServer 10.0\r\n"
    response += "\r\n"
    # 响应体
    # response += "响应体，给用户看"
    file = open('./baidu.html',"r")
    response += file.read()
    # 发送给客户端
    client.send(response.encode('UTF-8'))
    # 关闭连接
    client.close()



if __name__ == '__main__':
    print("Start!-----")
    # 创建socket对象
    tcp_socket = sk.socket(sk.AF_INET,sk.SOCK_STREAM)
    # 绑定主机地址
    tcp_socket.bind(('127.0.0.1',604))
    # 监听
    tcp_socket.listen(128)

    while 1:
        # 等待服务器连接
        clnt0,addr0 = tcp_socket.accept()
        print('连接到地址:', addr0)
        # 为客户端提供服务
        service_for_client(clnt0)
