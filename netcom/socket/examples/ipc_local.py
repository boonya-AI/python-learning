"""本地进程间通信示例"""
import sys
import os
import time
import threading

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from netipc.ipc.unix_socket import UnixSocketServer, UnixSocketClient
from netipc.ipc.pipe import NamedPipe


def demo_unix_socket():
    """演示 Unix Domain Socket 通信"""
    print("\n=== Unix Domain Socket 示例 ===")

    def message_handler(data):
        print(f"服务器收到: {data.decode('utf-8')}")
        return b"Processed: " + data

    # 启动服务器
    server = UnixSocketServer('/tmp/demo.sock')
    server_thread = threading.Thread(
        target=lambda: server.start(message_handler),
        daemon=True
    )
    server_thread.start()
    time.sleep(1)

    # 启动客户端
    client = UnixSocketClient('/tmp/demo.sock')
    client.connect()
    client.send("Hello from Unix Socket!")
    client.close()

    time.sleep(2)
    server.close()


def demo_named_pipe():
    """演示命名管道通信"""
    print("\n=== 命名管道示例 ===")

    pipe = NamedPipe("demo_pipe")

    def server_thread():
        server_sock = pipe.server.start()
        print("服务端: 等待数据...")
        data = pipe.server.read()
        print(f"服务端收到: {data.decode('utf-8')}")
        pipe.server.write(b"Response from server")
        time.sleep(1)
        pipe.server.close()

    # 启动服务端
    thread = threading.Thread(target=server_thread, daemon=True)
    thread.start()
    time.sleep(1)

    # 客户端连接
    client_sock = pipe.client.connect()
    pipe.client.write(b"Hello from client")
    response = pipe.client.read()
    print(f"客户端收到: {response.decode('utf-8')}")
    pipe.client.close()


if __name__ == "__main__":
    if sys.platform.startswith('win'):
        print("Unix Socket 在 Windows 上不支持，跳过演示")
        demo_named_pipe()
    else:
        demo_unix_socket()
        demo_named_pipe()