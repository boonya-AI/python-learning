"""UDP 服务器实现"""
import socket
import threading
from typing import Callable, Optional, Tuple


class UDPServer:
    """UDP 服务器 - 无连接协议"""

    def __init__(self, host: str = 'localhost', port: int = 8888):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.running = False
        self.message_callback: Optional[Callable] = None

    def start(self, callback: Optional[Callable] = None):
        """
        启动 UDP 服务器
        callback: 接收消息时的回调函数 callback(data, address)
        """
        self.sock.bind((self.host, self.port))
        self.running = True
        self.message_callback = callback
        print(f"UDP 服务器监听 {self.host}:{self.port}")

        try:
            while self.running:
                # UDP 不需要 accept，直接接收数据
                data, addr = self.sock.recvfrom(4096)
                print(f"收到来自 {addr} 的数据: {data.decode('utf-8')}")

                if self.message_callback:
                    self.message_callback(data, addr)
                else:
                    # 默认回显消息
                    self.sock.sendto(b"Echo: " + data, addr)
        except KeyboardInterrupt:
            print("\n服务器关闭")
        finally:
            self.close()

    def send_to(self, data: bytes, address: Tuple[str, int]):
        """发送数据到指定地址"""
        self.sock.sendto(data, address)

    def close(self):
        """关闭服务器"""
        self.running = False
        self.sock.close()