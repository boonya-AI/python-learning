import socket

class TCPClient:
    """简单的 TCP 客户端"""
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        """连接服务器"""
        self.sock.connect((self.host, self.port))
        print(f"已连接到 TCP 服务器 {self.host}:{self.port}")

    def send(self, message):
        """发送消息并接收回显"""
        self.sock.sendall(message.encode('utf-8'))
        response = self.sock.recv(1024)
        print(f"服务器响应：{response.decode('utf-8')}")

    def close(self):
        self.sock.close()