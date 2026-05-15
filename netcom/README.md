
## 网络和进程间通信
本章介绍的模块提供了网络和进程间通信的机制。

某些模块仅适用于同一台机器上的两个进程，例如 signal 和 mmap 。 其他模块支持两个或多个进程可用于跨机器通信的网络协议。

本章中描述的模块列表是：


[asyncio --- 异步 I/O](https://docs.python.org/zh-cn/3.14/library/asyncio.html)

[socket --- 低层级的网络接口](https://docs.python.org/zh-cn/3.14/library/socket.html)

[ssl --- 套接字对象的 TLS/SSL 包装器](https://docs.python.org/zh-cn/3.14/library/ssl.html)

[select --- 等待 I/O 完成](https://docs.python.org/zh-cn/3.14/library/select.html)

[selectors --- 高层级 I/O 复用](https://docs.python.org/zh-cn/3.14/library/selectors.html)

[signal --- 设置异步事件处理器](https://docs.python.org/zh-cn/3.14/library/signal.html)

[mmap --- 内存映射文件支持](https://docs.python.org/zh-cn/3.14/library/mmap.html)