import socket
import threading

class TCPServer:
    """简单的 TCP 服务器"""
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []  # 存储连接的客户端

    def start(self):
        """启动服务器"""
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"TCP 服务器监听 {self.host}:{self.port}")
        try:
            while True:
                client_sock, addr = self.sock.accept()
                print(f"客户端连接：{addr}")
                thread = threading.Thread(target=self._handle_client, args=(client_sock, addr))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\n服务器关闭")
        finally:
            self.sock.close()

    def _handle_client(self, client_sock, addr):
        """处理客户端消息"""
        while True:
            try:
                data = client_sock.recv(1024)
                if not data:
                    break
                print(f"收到 {addr}: {data.decode('utf-8')}")
                # 回显消息
                client_sock.sendall(f"Echo: {data.decode('utf-8')}".encode('utf-8'))
            except (ConnectionResetError, BrokenPipeError):
                break
        client_sock.close()
        print(f"客户端断开：{addr}")