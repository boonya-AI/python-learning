"""
演示 selectors 的 unregister() 方法

unregister(fileobj)
- 注销一个已注册的文件对象，停止对其的 I/O 事件监控
- 返回该文件对象关联的 SelectorKey
- 如果 fileobj 未注册会抛出 KeyError
- 文件对象在关闭前应先 unregister
"""

import selectors
import socket


def demo_unregister_basic():
    """基本注销演示"""
    print("=" * 50)
    print("unregister() 基本用法演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)
    sock.setblocking(False)

    # 注册
    sel.register(sock, selectors.EVENT_READ, data="my_socket")
    print(f"\n注册后: 已注册 {len(sel.get_map())} 个文件对象")

    # 注销 - 返回关联的 SelectorKey
    key = sel.unregister(sock)
    print(f"\n调用 unregister(sock) 返回:")
    print(f"  SelectorKey: fd={key.fd}, events={key.events}, data={key.data!r}")
    print(f"  注销后: 已注册 {len(sel.get_map())} 个文件对象")

    # 清理
    sel.close()
    sock.close()
    print("\n资源已清理")


def demo_unregister_errors():
    """演示注销时可能发生的错误"""
    print("\n" + "=" * 50)
    print("unregister() 错误处理演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)
    sock.setblocking(False)

    # 尝试注销未注册的 socket
    print("\n1. 注销未注册的 socket:")
    try:
        sel.unregister(sock)
    except KeyError as e:
        print(f"   KeyError: {e}")

    # 注册后注销，再次注销
    sel.register(sock, selectors.EVENT_READ)
    sel.unregister(sock)
    print("\n2. 重复注销:")
    try:
        sel.unregister(sock)
    except KeyError as e:
        print(f"   KeyError: {e}")

    # 清理
    sel.close()
    sock.close()
    print("\n资源已清理")


def demo_unregister_before_close():
    """演示先注销再关闭 socket 的最佳实践"""
    print("\n" + "=" * 50)
    print("最佳实践: 先 unregister 再 close")
    print("=" * 50)

    sel = selectors.DefaultSelector()
    sockets = []

    # 创建并注册多个 socket
    for i in range(3):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 0))
        sock.listen(1)
        sock.setblocking(False)
        sockets.append(sock)
        sel.register(sock, selectors.EVENT_READ, data=f"socket_{i}")

    print(f"\n初始状态: 已注册 {len(sel.get_map())} 个文件对象")

    # 逐个注销并关闭
    for i, sock in enumerate(sockets):
        sel.unregister(sock)
        sock.close()
        print(f"  注销并关闭 socket_{i}，剩余: {len(sel.get_map())} 个")

    sel.close()
    print("\n全部清理完成")


if __name__ == "__main__":
    demo_unregister_basic()
    demo_unregister_errors()
    demo_unregister_before_close()
