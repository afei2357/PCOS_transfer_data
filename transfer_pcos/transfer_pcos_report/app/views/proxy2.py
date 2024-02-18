import requests
import socks
import socket

# 设置代理
#socks.set_default_proxy(socks.SOCKS5, "localhost", 1080)
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 1080)
socket.socket = socks.socksocket

# 设置请求头
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}

# 发送请求
response = requests.get("https://www.google.com", headers=headers)

# 输出响应内容
print(response.content)
