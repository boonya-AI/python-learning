"""
回声服务器的测试客户端

用于测试 echo_server.py

运行方式:
    先启动服务器: python -m selectors_demo.servers.echo_server
    再运行客户端: python -m selectors_demo.clients.echo_client
"""

import socket
import sys


def main(host='localhost', port=9999):
    """连接到回声服务器并进行交互"""
    print("=" * 50)
    print("回声服务器测试客户端")
    print("=" * 50)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))
        print(f"\n已连接到 {host}:{port}")
        print("输入消息按回车发送，输入 'quit' 退出\n")

        while True:
            msg = input(">>> ")
            if msg.lower() == 'quit':
                break
            if not msg:
                continue

            sock.send(msg.encode('utf-8'))
            data = sock.recv(4096)
            print(f"<<< 服务器回送: {data.decode('utf-8')}")

    except ConnectionRefusedError:
        print(f"\n连接失败: 服务器 {host}:{port} 未运行")
        print("请先启动服务器: python -m selectors_demo.servers.echo_server")
    except KeyboardInterrupt:
        print("\n\n客户端退出")
    finally:
        sock.close()
        print("连接已关闭")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
    main(port=port)
