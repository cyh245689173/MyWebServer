import socket
import os
import threading

#主线程负责接受客户端请求，子线程负责和客户端收发消息





class HttpWebServer(object):
    def __init__(self):
        # 创建tcp服务端套结字
        tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 设置端口号复用，程序退出端口号立即释放
        tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定端口号
        tcp_server_socket.bind(('', 8000))
        # 设置监听
        tcp_server_socket.listen(128)
        # 循环等待接受客户端的连接请求
        #把tcp服务器的套结字作为web服务器对象的属性
        self.tcp_server_socket = tcp_server_socket


    #启动服务器方法
    def start(self):
        while True:
            # 等待接受客户端链接请求
            new_socket, ip_port = self.tcp_server_socket.accept()
            # 代码执行到此，说明连接建立成功

            sub_thread = threading.Thread(target=self.handle_client_request, args=(new_socket,))
            # 设置成为守护主线程,主线程结束，子线程跟着结束，不再收发消息
            sub_thread.setDaemon(True)
            # 启动子线程，执行的对应的任务
            sub_thread.start()

    # 处理客户端请求
    @staticmethod
    def handle_client_request(new_socket):
        # 接受客户端的请求信息
        recv_data = new_socket.recv(4096)
        # 判断接受的数据是否为空，如果为空，关闭套结字
        if len(recv_data) == 0:
            new_socket.close()
            return

        # 对二进制数据进行解码
        recv_content = recv_data.decode('utf8')
        print(recv_content)

        # 对数据按照空格进行分割
        request_list = recv_content.split(' ', maxsplit=2)
        # 获取请求的资源路径
        request_path = request_list[1]
        print(request_path)

        if request_path == '/':
            request_path = '/index.html'

        # 1.os.path.exits
        # os.path.exists("static" + request_path)
        # 2.异常
        try:
            # 打开文件读取文件数据,提示：这里使用rb模式，兼容打开图片文件
            with open("static" + request_path, 'rb') as file:
                file_data = file.read()
        except Exception as e:
            # 代码执行到此处，表示没有请求的文件，返回404信息
            # 响应行
            response_line = 'HTTP/1.1 404 Not Found\r\n'
            # 响应头
            response_header = "Server:CYH1.0\r\n"

            with open("static/error.html", 'rb') as file:
                file_data = file.read()
                # 响应体
                response_body = file_data

                response = (response_line + response_header + '\r\n').encode('utf8') + response_body

                # 发送给浏览器的相应报文数据
                new_socket.send(response)


        else:
            # 代码执行到此，表示文件存在，返回状态200信息
            # 把数据封装成http相应报文格式的数据

            # 响应行
            response_line = 'HTTP/1.1 200 OK\r\n'
            # 响应头
            response_header = "Server:CYH1.0\r\n"
            # 响应体
            response_body = file_data

            response = (response_line + response_header + '\r\n').encode('utf8') + response_body

            # 发送给浏览器的相应报文数据
            new_socket.send(response)
        finally:
            # 关闭服务于客户端的套结字
            new_socket.close()








# 判断是否是主模块
if __name__ == '__main__':
    web_server = HttpWebServer()
    #启动服务器
    web_server.start()
