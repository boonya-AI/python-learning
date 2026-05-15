import socket
import ssl
import threading
from typing import Callable, Optional
from .ssl_context import create_server_context


class SSLServer:
    """支持 SSL/TLS 加密的安全 TCP 服务器"""

    def __init__(self, host: str = 'localhost', port: int = 8443,
                 cert_path: str = 'certs/server.crt',
                 key_path: str = 'certs/server.key',
                 ca_cert_path: Optional[str] = None,
                 require_client_cert: bool = False):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 创建 SSL 上下文
        self.context = create_server_context(
            cert_path, key_path, ca_cert_path, require_client_cert
        )
        self.running = False
        self.message_callback: Optional[Callable] = None

    def start(self, callback: Optional[Callable] = None):
        """启动 SSL 服务器"""
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.running = True
        self.message_callback = callback
        print(f"SSL 服务器监听 {self.host}:{self.port} (TLS 加密)")

        try:
            while self.running:
                client_sock, addr = self.sock.accept()
                # 将普通 socket 升级为 SSL socket
                ssl_client = self.context.wrap_socket(client_sock, server_side=True)
                print(f"SSL 客户端连接: {addr}, 加密版本: {ssl_client.version()}")

                thread = threading.Thread(target=self._handle_client,
                                          args=(ssl_client, addr))
                thread.daemon = True
                thread.start()
        except KeyboardInterrupt:
            print("\nSSL 服务器关闭")
        finally:
            self.close()

    def _handle_client(self, ssl_client: ssl.SSLSocket, addr):
        """处理 SSL 客户端连接"""
        try:
            while self.running:
                data = ssl_client.recv(1024)
                if not data:
                    break

                message = data.decode('utf-8')
                print(f"收到 {addr}: {message}")

                if self.message_callback:
                    self.message_callback(message, addr, ssl_client)
                else:
                    # 默认回显加密消息
                    response = f"SSL Echo: {message}".encode('utf-8')
                    ssl_client.sendall(response)
        except (ssl.SSLError, ConnectionResetError) as e:
            print(f"SSL 错误: {e}")
        finally:
            ssl_client.close()
            print(f"SSL 客户端断开: {addr}")

    def close(self):
        """关闭服务器"""
        self.running = False
        self.sock.close()