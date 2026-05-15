#!/usr/bin/env python3
"""
select 模块示例统一演示入口
"""

import sys
import os
import threading
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def print_banner():
    print("=" * 50)
    print("    select 模块 I/O 多路复用示例")
    print("=" * 50)
    print("\n可用的示例:")
    print("1. select.select() - 基础多路复用服务器")
    print("2. select.poll() - 高性能服务器")
    print("3. select.epoll() - Linux 高并发服务器")
    print("4. 多客户端测试工具")
    print("5. 聊天室服务器 (完整示例)")
    print("6. 对比测试 (同时运行多种服务器)")
    print("0. 退出")
    print("-" * 50)


def run_select_server():
    from netipc.select_examples.simple_select_server import SimpleSelectServer
    server = SimpleSelectServer()
    server.start()


def run_poll_server():
    from netipc.select_examples.poll_server import PollServer
    server = PollServer()
    server.start()


def run_epoll_server():
    if not hasattr(sys.modules['select'], 'epoll'):
        print("错误: epoll 仅支持 Linux 系统")
        return
    from netipc.select_examples.epoll_server import EpollServer
    use_edge = input("使用边缘触发模式？(y/n, 默认 n): ").lower() == 'y'
    server = EpollServer(edge_trigger=use_edge)
    server.start()


def run_client_test():
    from netipc.select_examples.echo_client import EchoClient, MultiClientTest
    print("\n1. 单客户端交互模式")
    print("2. 多客户端并发测试")
    choice = input("请选择 (1-2): ")

    if choice == '1':
        client = EchoClient()
        client.interactive_mode()
    elif choice == '2':
        num = int(input("客户端数量 (默认5): ") or "5")
        MultiClientTest.run_test(num_clients=num)


def run_chat_server():
    from netipc.select_examples.multi_chat_server import ChatRoomServer
    server = ChatRoomServer()
    server.start()


def run_comparison_test():
    """运行对比测试：启动三种服务器并测试性能"""
    print("\n对比测试说明：")
    print("此测试会依次启动 select/poll/epoll 服务器")
    print("每个服务器会处理 10 个并发客户端连接")
    print("请注意：epoll 仅在 Linux 下可用\n")

    from netipc.select_examples.echo_client import MultiClientTest
    from netipc.select_examples.simple_select_server import SimpleSelectServer
    from netipc.select_examples.poll_server import PollServer

    servers = [("Select", SimpleSelectServer, 8881), ("Poll", PollServer, 8882)]

    if hasattr(sys.modules['select'], 'epoll'):
        from netipc.select_examples.epoll_server import EpollServer
        servers.append(("Epoll", EpollServer, 8883))

    for name, server_class, port in servers:
        print(f"\n测试 {name} 服务器 (端口 {port})...")
        server = server_class(port=port)
        server_thread = threading.Thread(target=server.start, daemon=True)
        server_thread.start()
        time.sleep(1)

        # 运行客户端测试
        MultiClientTest.run_test(port=port, num_clients=10)

        # 停止服务器（强制关闭）
        try:
            server._cleanup()
        except:
            pass
        time.sleep(1)

    print("\n对比测试完成!")


def main():
    while True:
        print_banner()
        choice = input("\n请选择功能 (0-6): ").strip()

        if choice == '0':
            print("感谢使用！")
            break
        elif choice == '1':
            run_select_server()
        elif choice == '2':
            run_poll_server()
        elif choice == '3':
            run_epoll_server()
        elif choice == '4':
            run_client_test()
        elif choice == '5':
            run_chat_server()
        elif choice == '6':
            run_comparison_test()
        else:
            print("无效选择，请重试")

        print("\n" + "=" * 50)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
        sys.exit(0)