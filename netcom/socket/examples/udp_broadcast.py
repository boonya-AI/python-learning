"""UDP 广播示例 - 发现局域网服务"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import socket
import time
from netipc.udp.server import UDPServer
from netipc.udp.client import UDPClient


class UDPBroadcastServer(UDPServer):
    """支持广播发现的 UDP 服务器"""

    def start(self):
        """启动服务器并响应广播发现请求"""
        self.sock.bind((self.host, self.port))
        self.running = True
        print(f"UDP 广播服务器运行在 {self.host}:{self.port}")

        while self.running:
            try:
                data, addr = self.sock.recvfrom(4096)
                message = data.decode('utf-8')

                if message == "DISCOVER":
                    response = f"SERVER:{socket.gethostname()}:{self.port}"
                    self.sock.sendto(response.encode('utf-8'), addr)
                    print(f"响应发现请求: {addr}")
                else:
                    print(f"收到消息: {message} from {addr}")
                    self.sock.sendto(b"Echo: " + data, addr)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"错误: {e}")


def broadcast_discovery():
    """广播发现请求，查找网络中的服务"""
    client = UDPClient()

    print("正在广播发现请求...")
    # 使用广播地址
    client.send("DISCOVER", host='<broadcast>', port=8888)

    # 等待响应
    try:
        while True:
            data, addr = client.sock.recvfrom(4096)
            print(f"发现服务: {data.decode('utf-8')} at {addr}")
    except socket.timeout:
        print("发现完成")


if __name__ == "__main__":
    choice = input("选择模式 (1: 广播服务器, 2: 发现客户端): ")
    if choice == '1':
        server = UDPBroadcastServer(port=8888)
        server.start()
    else:
        broadcast_discovery()