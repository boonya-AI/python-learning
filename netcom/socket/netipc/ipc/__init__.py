"""本地进程间通信模块"""
from .unix_socket import UnixSocketServer, UnixSocketClient
from .pipe import NamedPipe

__all__ = ['UnixSocketServer', 'UnixSocketClient', 'NamedPipe']