"""单元测试"""
import unittest
import threading
import time
import tempfile
import os

from netipc.tcp.server import TCPServer
from netipc.tcp.client import TCPClient
from netipc.udp.server import UDPServer
from netipc.udp.client import UDPClient
from netipc.utils.helpers import encode_message, decode_message, get_local_ip


class TestTCPCommunication(unittest.TestCase):
    """TCP 通信测试"""

    def setUp(self):
        self.server = TCPServer(port=18888)
        self.server_thread = threading.Thread(target=self.server.start, daemon=True)
        self.server_thread.start()
        time.sleep(0.5)

    def test_client_server_echo(self):
        client = TCPClient(port=18888)
        client.connect()

        # 修改客户端发送方法以接收响应
        client.sock.sendall(b"Hello")
        response = client.sock.recv(1024)

        self.assertEqual(response, b"Echo: Hello")
        client.close()

    def tearDown(self):
        self.server.sock.close()


class TestUDPCommunication(unittest.TestCase):
    """UDP 通信测试"""

    def setUp(self):
        self.server = UDPServer(port=18889)
        self.server_thread = threading.Thread(target=self.server.start, daemon=True)
        self.server_thread.start()
        time.sleep(0.5)

    def test_udp_echo(self):
        client = UDPClient()
        # 修改客户端以等待响应
        client.sock.settimeout(2)
        client.send("Hello UDP", port=18889)
        # 注意：需要在实际实现中等待响应

        client.close()

    def tearDown(self):
        self.server.close()


class TestUtils(unittest.TestCase):
    """工具函数测试"""

    def test_encode_decode(self):
        msg = "Hello World"
        encoded = encode_message(msg)
        decoded = decode_message(encoded)
        self.assertEqual(msg, decoded)

    def test_json_encode_decode(self):
        data = {"key": "value", "number": 42}
        encoded = encode_message(data)
        decoded = decode_message(encoded, as_json=True)
        self.assertEqual(data, decoded)

    def test_get_local_ip(self):
        ip = get_local_ip()
        self.assertIsInstance(ip, str)
        self.assertTrue(ip.count('.') == 3 or ip == '127.0.0.1')


if __name__ == "__main__":
    unittest.main()