"""
演示 selectors 的 get_key() 和 get_map() 方法

get_key(fileobj)
- 返回与已注册文件对象关联的 SelectorKey
- 如果 fileobj 未注册，抛出 KeyError

get_map()
- 返回一个从文件对象到 SelectorKey 的只读映射（Mapping）
- 可用于查看所有已注册的文件对象
"""

import selectors
import socket


def demo_get_key():
    """演示 get_key() 方法"""
    print("=" * 50)
    print("get_key() 方法演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock1.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock1.bind(('localhost', 0))
    sock1.listen(1)
    sock1.setblocking(False)

    sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock2.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock2.bind(('localhost', 0))
    sock2.listen(1)
    sock2.setblocking(False)

    # 注册两个 socket
    sel.register(sock1, selectors.EVENT_READ, data="socket_1")
    sel.register(sock2, selectors.EVENT_READ | selectors.EVENT_WRITE, data="socket_2")

    # 使用 get_key 查询
    print("\n查询 sock1 的 SelectorKey:")
    key1 = sel.get_key(sock1)
    print(f"  fd={key1.fd}, events={key1.events}, data={key1.data!r}")

    print("\n查询 sock2 的 SelectorKey:")
    key2 = sel.get_key(sock2)
    print(f"  fd={key2.fd}, events={key2.events}, data={key2.data!r}")

    # 查询未注册的 socket
    print("\n查询未注册的 socket:")
    unregistered = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sel.get_key(unregistered)
    except KeyError as e:
        print(f"  KeyError: {e}")
    unregistered.close()

    # 清理
    sel.unregister(sock1)
    sel.unregister(sock2)
    sel.close()
    sock1.close()
    sock2.close()
    print("\n资源已清理")


def demo_get_map():
    """演示 get_map() 方法"""
    print("\n" + "=" * 50)
    print("get_map() 方法演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    sockets = []
    for i in range(4):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind(('localhost', 0))
        sock.listen(1)
        sock.setblocking(False)
        sockets.append(sock)
        sel.register(sock, selectors.EVENT_READ, data=f"server_{i}")

    # get_map() 返回一个 Mapping
    mapping = sel.get_map()
    print(f"\nget_map() 返回类型: {type(mapping)}")
    print(f"映射中的条目数: {len(mapping)}")

    # 遍历所有已注册的文件对象
    print("\n遍历所有已注册项:")
    for fileobj, key in mapping.items():
        print(f"  fileobj={fileobj}, fd={key.fd}, data={key.data!r}")

    # 检查某个 socket 是否在映射中
    print(f"\nsockets[0] 是否已注册: {sockets[0] in mapping}")

    # 通过文件对象索引获取 key
    key = mapping[sockets[2]]
    print(f"通过索引访问 mapping[sockets[2]]: data={key.data!r}")

    # 注销一个后再查看
    sel.unregister(sockets[1])
    print(f"\n注销 sockets[1] 后映射条目数: {len(sel.get_map())}")
    print(f"sockets[1] 是否还在映射中: {sockets[1] in sel.get_map()}")

    # 清理
    for sock in sockets:
        if sock in sel.get_map():
            sel.unregister(sock)
        sock.close()
    sel.close()
    print("\n资源已清理")


def demo_get_map_readonly():
    """演示 get_map() 返回的是只读映射"""
    print("\n" + "=" * 50)
    print("get_map() 只读特性演示")
    print("=" * 50)

    sel = selectors.DefaultSelector()

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('localhost', 0))
    sock.listen(1)
    sock.setblocking(False)

    sel.register(sock, selectors.EVENT_READ, data="test")

    mapping = sel.get_map()

    # 尝试修改映射（应该失败）
    print("\n尝试直接修改映射:")
    try:
        mapping[sock] = "something"
    except TypeError as e:
        print(f"  TypeError: {type(mapping).__name__} 不支持直接赋值")

    print("\n结论: get_map() 返回只读视图，要修改需使用 modify() 或 unregister()+register()")

    # 清理
    sel.unregister(sock)
    sel.close()
    sock.close()
    print("\n资源已清理")


if __name__ == "__main__":
    demo_get_key()
    demo_get_map()
    demo_get_map_readonly()
