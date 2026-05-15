"""通用辅助工具函数"""
import socket
import json
from typing import Union, Tuple, Optional

def encode_message(data: Union[str, dict, bytes]) -> bytes:
    """
    编码消息为字节流
    支持：字符串、字典、字节
    """
    if isinstance(data, bytes):
        return data
    elif isinstance(data, dict):
        return json.dumps(data).encode('utf-8')
    elif isinstance(data, str):
        return data.encode('utf-8')
    else:
        raise TypeError(f"不支持的数据类型: {type(data)}")

def decode_message(data: bytes, as_json: bool = False) -> Union[str, dict]:
    """
    解码字节流消息
    as_json: True 时尝试解析为 JSON，否则返回字符串
    """
    try:
        decoded = data.decode('utf-8')
        if as_json:
            return json.loads(decoded)
        return decoded
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        raise ValueError(f"消息解码失败: {e}")

def resolve_address(host: str, port: int) -> Tuple[str, int]:
    """
    解析主机名为 IP 地址
    返回 (ip, port)
    """
    try:
        ip = socket.gethostbyname(host)
        return (ip, port)
    except socket.gaierror:
        raise ValueError(f"无法解析主机名: {host}")

def get_local_ip() -> str:
    """获取本机局域网 IP 地址"""
    try:
        # 创建一个 UDP socket 连接到外部地址（不实际发送数据）
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def validate_port(port: int) -> bool:
    """验证端口号是否有效（1-65535）"""
    return 1 <= port <= 65535

def format_bytes(size: int) -> str:
    """格式化字节大小为人类可读的格式"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} TB"