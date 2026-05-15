"""
自动化测试客户端 - 用于自动验证服务器功能

无需交互输入，自动连接、发送、接收、验证
"""

import socket
import time
import threading
import sys


def test_echo_server(host='localhost', port=9999):
    """自动测试回声服务器"""
    print("=" * 50)
    print("自动测试: 回声服务器")
    print("=" * 50)

    test_messages = [
        b"Hello, World!",
        b"Test message 123",
        b"selectors module demo",
        "中文测试消息".encode('utf-8'),
    ]

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print(f"\n已连接到 {host}:{port}")

        passed = 0
        failed = 0

        for msg in test_messages:
            sock.send(msg)
            time.sleep(0.1)
            response = sock.recv(4096)

            if response == msg:
                print(f"  [PASS] 发送: {msg!r} -> 回收: {response!r}")
                passed += 1
            else:
                print(f"  [FAIL] 发送: {msg!r} -> 回收: {response!r}")
                failed += 1

        sock.close()
        print(f"\n测试结果: {passed} 通过, {failed} 失败")
        return failed == 0

    except ConnectionRefusedError:
        print(f"\n连接失败: 服务器 {host}:{port} 未运行")
        return False


def test_multi_client(host='localhost', port=9999, num_clients=5):
    """测试多客户端并发连接"""
    print("\n" + "=" * 50)
    print(f"自动测试: {num_clients} 个并发客户端")
    print("=" * 50)

    results = []

    def client_task(client_id):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            msg = f"Client {client_id} message".encode()
            sock.send(msg)
            time.sleep(0.1)
            response = sock.recv(4096)
            success = response == msg
            results.append((client_id, success, msg, response))
            sock.close()
        except Exception as e:
            results.append((client_id, False, None, str(e)))

    try:
        threads = []
        for i in range(num_clients):
            t = threading.Thread(target=client_task, args=(i,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join(timeout=5)

        passed = sum(1 for _, success, _, _ in results if success)
        failed = len(results) - passed

        for client_id, success, msg, response in sorted(results):
            status = "PASS" if success else "FAIL"
            print(f"  [{status}] Client {client_id}: {msg!r} -> {response!r}")

        print(f"\n测试结果: {passed} 通过, {failed} 失败 (共 {num_clients} 客户端)")
        return failed == 0

    except ConnectionRefusedError:
        print(f"\n连接失败: 服务器 {host}:{port} 未运行")
        return False


if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 9999
    test_echo_server(port=port)
    test_multi_client(port=port)
