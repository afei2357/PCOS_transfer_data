import requests
import socks
import socket

#socks.set_default_proxy(socks.SOCKS5, "localhost", 1080)
#socket.socket = socks.socksocket

proxies = {
        "http": "socks5://localhost:1080",
            "https": "socks5://localhost:1080"
}

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}

response = requests.get("https://www.google.com", headers=headers, proxies=proxies)

print(response.content)
