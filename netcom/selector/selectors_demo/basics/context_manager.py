"""
演示 selectors 模块的上下文管理器协议

BaseSelector 及其子类都支持 with 语句（上下文管理器协议），
退出 with 块时会自动调用 close() 释放资源。
"""

import selectors
import socket


def demo_context_manager():
    """演示使用 with 语句自动管理 selector 生命周期"""
    print("=" * 50)
    print("Selector 上下文管理器演示")
    print("=" * 50)

    # 使用 with 语句，退出时自动 close
    with selectors.DefaultSelector() as sel:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 0))
        sock.listen(1)
        sock.setblocking(False)
        port = sock.getsockname()[1]

        sel.register(sock, selectors.EVENT_READ, data="server")
        print(f"\n在 with 块内:")
        print(f"  已注册 socket，端口: {port}")
        print(f"  get_map() 有 {len(sel.get_map())} 个注册项")

        # 创建客户端触发事件
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(('localhost', port))

        events = sel.select(timeout=1)
        print(f"  select() 返回 {len(events)} 个就绪事件")

        # 清理 socket（selector 会在 with 退出时自动关闭）
        sel.unregister(sock)
        client.close()
        sock.close()

    # with 块退出后，selector 已自动关闭
    print(f"\n退出 with 块后:")
    print(f"  selector 已自动关闭（调用了 close()）")

    # 尝试在关闭后使用会报错
    try:
        sel.register(sock, selectors.EVENT_READ)
    except (RuntimeError, ValueError, OSError) as e:
        print(f"  关闭后尝试使用报错: {type(e).__name__}: {e}")


def demo_without_context_manager():
    """对比：不使用上下文管理器时需要手动 close"""
    print("\n" + "=" * 50)
    print("不使用上下文管理器（手动管理）对比")
    print("=" * 50)

    sel = selectors.DefaultSelector()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)
    sock.setblocking(False)

    try:
        sel.register(sock, selectors.EVENT_READ)
        print(f"\n手动管理模式:")
        print(f"  注册成功，有 {len(sel.get_map())} 个注册项")
    finally:
        # 必须手动清理
        sel.unregister(sock)
        sel.close()
        sock.close()
        print(f"  在 finally 中手动调用了 close()")

    print("\n推荐使用 with 语句，更安全、更简洁！")


if __name__ == "__main__":
    demo_context_manager()
    demo_without_context_manager()
