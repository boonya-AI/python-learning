import ssl
import os
from typing import Optional


def create_server_context(cert_path: str, key_path: str,
                          ca_cert_path: Optional[str] = None,
                          require_client_cert: bool = False) -> ssl.SSLContext:
    """
    创建服务端 SSL 上下文

    Args:
        cert_path: 服务器证书文件路径
        key_path: 服务器私钥文件路径
        ca_cert_path: CA 证书路径（用于验证客户端）
        require_client_cert: 是否需要客户端证书验证

    Returns:
        配置好的 SSLContext
    """
    # 使用 TLS 1.2+ 协议
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)

    # 加载证书和私钥
    context.load_cert_chain(cert_path, key_path)

    # 设置加密套件（平衡安全性与兼容性）
    context.set_ciphers('ECDHE+AESGCM:ECDHE+CHACHA20:DHE+AESGCM:!aNULL:!MD5:!DSS')

    if require_client_cert and ca_cert_path:
        # 验证客户端证书
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(ca_cert_path)
    else:
        context.verify_mode = ssl.CERT_NONE

    return context


def create_client_context(ca_cert_path: Optional[str] = None,
                          check_hostname: bool = True) -> ssl.SSLContext:
    """
    创建客户端 SSL 上下文

    Args:
        ca_cert_path: CA 证书路径（用于验证服务器）
        check_hostname: 是否验证主机名

    Returns:
        配置好的 SSLContext
    """
    # 创建默认的客户端上下文
    context = ssl.create_default_context()

    if ca_cert_path:
        # 使用自定义 CA 验证服务器证书
        context.load_verify_locations(ca_cert_path)
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = check_hostname
    else:
        # 使用系统默认 CA 证书
        context.verify_mode = ssl.CERT_NONE
        context.check_hostname = False

    return context


def wrap_socket_safely(sock, context: ssl.SSLContext,
                       server_hostname: str = None,
                       is_server: bool = False) -> ssl.SSLSocket:
    """
    安全地包装普通 socket 为 SSL socket

    Args:
        sock: 原始 socket 对象
        context: SSL 上下文
        server_hostname: 服务器主机名（客户端需要）
        is_server: 是否为服务端模式

    Returns:
        SSL Socket 对象
    """
    if is_server:
        return context.wrap_socket(sock, server_side=True)
    else:
        return context.wrap_socket(sock, server_hostname=server_hostname)