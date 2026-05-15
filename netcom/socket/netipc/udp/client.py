"""UDP 客户端实现"""
import socket
from typing import Optional, Tuple


class UDPClient:
    """UDP 客户端 - 无连接通信"""

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(5.0)  # 5秒超时

    def send(self, message: str, host: str = 'localhost', port: int = 8888):
        """发送 UDP 消息"""
        addr = (host, port)
        self.sock.sendto(message.encode('utf-8'), addr)
        print(f"发送到 {host}:{port}: {message}")

        try:
            # 尝试接收响应（UDP 可能无响应）
            data, server_addr = self.sock.recvfrom(4096)
            print(f"收到响应: {data.decode('utf-8')}")
            return data
        except socket.timeout:
            print("未收到响应（超时）")
            return None

    def send_with_response(self, message: str, host: str = 'localhost',
                           port: int = 8888, timeout: float = 5.0) -> Optional[bytes]:
        """发送消息并等待响应"""
        self.sock.settimeout(timeout)
        return self.send(message, host, port)

    def close(self):
        """关闭客户端"""
        self.sock.close()