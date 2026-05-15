"""
聊天服务器的测试客户端

用于测试 chat_server.py，支持同时收发消息

运行方式:
    先启动服务器: python -m selectors_demo.servers.chat_server
    再运行客户端: python -m selectors_demo.clients.chat_client
"""

import socket
import sys
import threading


def receive_messages(sock):
    """接收线程：持续接收服务器消息"""
    while True:
        try:
            data = sock.recv(4096)
            if not data:
                print("\n[断开] 服务器已关闭连接")
                break
            print(f"\r{data.decode('utf-8').strip()}")
            print(">>> ", end="", flush=True)
        except (ConnectionResetError, OSError):
            print("\n[断开] 连接已中断")
            break


def main(host='localhost', port=9998):
    """连接到聊天服务器"""
    print("=" * 50)
    print("聊天服务器测试客户端")
    print("=" * 50)

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((host, port))
        print(f"\n已连接到聊天室 {host}:{port}")
        print("输入消息按回车发送，输入 'quit' 退出\n")

        # 启动接收线程
        recv_thread = threading.Thread(target=receive_messages, args=(sock,), daemon=True)
        recv_thread.start()

        while True:
            msg = input(">>> ")
            if msg.lower() == 'quit':
                break
            if not msg:
                continue
            try:
                sock.send(msg.encode('utf-8'))
            except (BrokenPipeError, OSError):
                print("[错误] 发送失败，连接已断开")
                break

    except ConnectionRefusedError:
        print(f"\n连接失败: 服务器 {host}:{port} 未运行")
        print("请先启动服务器: python -m selectors_demo.servers.chat_server")
    except KeyboardInterrupt:
        print("\n\n客户端退出")
    finally:
        sock.close()
        print("连接已关闭")


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9998
    main(port=port)
