import socket
import ssl
from typing import Optional
from .ssl_context import create_client_context


class SSLClient:
    """SSL/TLS 加密的 TCP 客户端"""

    def __init__(self, host: str = 'localhost', port: int = 8443,
                 ca_cert_path: Optional[str] = None,
                 check_hostname: bool = True):
        self.host = host
        self.port = port
        self.ca_cert_path = ca_cert_path
        self.check_hostname = check_hostname
        self.sock: Optional[ssl.SSLSocket] = None
        self.context = create_client_context(ca_cert_path, check_hostname)

    def connect(self) -> bool:
        """连接到 SSL 服务器，返回连接是否成功"""
        try:
            # 创建普通 TCP 连接
            raw_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            raw_sock.connect((self.host, self.port))

            # 升级为 SSL 连接
            self.sock = self.context.wrap_socket(
                raw_sock, server_hostname=self.host
            )

            print(f"已连接到 SSL 服务器 {self.host}:{self.port}")
            print(f"TLS 版本: {self.sock.version()}")
            print(f"加密套件: {self.sock.cipher()}")

            # 可选：显示服务器证书信息
            cert = self.sock.getpeercert()
            if cert:
                print(f"服务器证书主题: {cert.get('subject', '')}")

            return True

        except ssl.SSLError as e:
            print(f"SSL 握手失败: {e}")
            return False
        except Exception as e:
            print(f"连接失败: {e}")
            return False

    def send(self, message: str) -> Optional[bytes]:
        """发送加密消息并接收响应"""
        if not self.sock:
            print("未连接到服务器")
            return None

        try:
            self.sock.sendall(message.encode('utf-8'))
            response = self.sock.recv(1024)
            print(f"服务器响应: {response.decode('utf-8')}")
            return response
        except ssl.SSLError as e:
            print(f"SSL 发送错误: {e}")
            return None
        except Exception as e:
            print(f"发送错误: {e}")
            return None

    def close(self):
        """安全关闭 SSL 连接"""
        if self.sock:
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
            except:
                pass