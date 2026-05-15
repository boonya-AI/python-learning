#!/usr/bin/env python3
"""
netipc 演示程序主入口
提供交互式菜单选择运行各种通信示例
"""

import sys
import os

# 添加项目根目录到 Python 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def print_banner():
    """打印程序横幅"""
    print("=" * 50)
    print("     netipc - 网络与进程间通信示例套件")
    print("=" * 50)
    print("\n可用示例:")
    print("1. TCP 聊天服务器/客户端")
    print("2. UDP 广播发现服务")
    print("3. Unix Domain Socket (本地IPC)")
    print("4. 命名管道通信")
    print("5. TCP 基础通信演示")
    print("6. UDP 基础通信演示")
    print("0. 退出")
    print("-" * 50)


def run_tcp_chat():
    """运行 TCP 聊天示例"""
    from examples import tcp_chat
    tcp_chat.main()


def run_udp_broadcast():
    """运行 UDP 广播示例"""
    from examples import udp_broadcast

    choice = input("\n选择模式 (1: 服务器, 2: 发现客户端): ")
    if choice == '1':
        from netipc.udp.server import UDPServer
        server = UDPServer(port=8888)
        server.start()
    else:
        from examples.udp_broadcast import broadcast_discovery
        broadcast_discovery()


def run_unix_socket():
    """运行 Unix Socket 示例"""
    from examples import ipc_local

    if sys.platform.startswith('win'):
        print("Unix Socket 在 Windows 上不支持")
    else:
        from netipc.ipc.unix_socket import UnixSocketServer, UnixSocketClient
        import threading
        import time

        def message_handler(data):
            print(f"收到: {data.decode('utf-8')}")

        server = UnixSocketServer('/tmp/demo.sock')
        server_thread = threading.Thread(target=server.start, args=(message_handler,))
        server_thread.daemon = True
        server_thread.start()
        time.sleep(1)

        client = UnixSocketClient('/tmp/demo.sock')
        client.connect()
        client.send("Hello from demo!")
        client.close()
        time.sleep(1)
        server.close()


def run_named_pipe():
    """运行命名管道示例"""
    from examples import ipc_local
    ipc_local.demo_named_pipe()


def run_tcp_basic():
    """运行 TCP 基础通信演示"""
    import threading
    import time
    from netipc.tcp.server import TCPServer
    from netipc.tcp.client import TCPClient

    server = TCPServer(port=9999)
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    time.sleep(1)

    client = TCPClient(port=9999)
    client.connect()
    client.send("Hello, TCP Server!")
    client.close()

    input("\n按回车键返回主菜单...")


def run_udp_basic():
    """运行 UDP 基础通信演示"""
    import threading
    import time
    from netipc.udp.server import UDPServer
    from netipc.udp.client import UDPClient

    server = UDPServer(port=8888)
    server_thread = threading.Thread(target=server.start, daemon=True)
    server_thread.start()
    time.sleep(1)

    client = UDPClient()
    client.send("Hello, UDP Server!", port=8888)
    client.close()

    input("\n按回车键返回主菜单...")


def main():
    """主程序"""
    while True:
        print_banner()
        choice = input("\n请选择功能 (0-6): ").strip()

        if choice == '0':
            print("感谢使用，再见！")
            break
        elif choice == '1':
            run_tcp_chat()
        elif choice == '2':
            run_udp_broadcast()
        elif choice == '3':
            run_unix_socket()
        elif choice == '4':
            run_named_pipe()
        elif choice == '5':
            run_tcp_basic()
        elif choice == '6':
            run_udp_basic()
        else:
            print("无效选择，请重试！")

        print("\n" + "=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)