import requests

proxy = {
    'http': 'socks5://127.0.0.1:1080',
    'https': 'socks5://127.0.0.1:1080'
    #'http': 'http://127.0.0.1:1081',
    #'https': 'https://127.0.0.1:1081'
}

url = 'http://www.google.com'

response = requests.get(url, proxies=proxy)
print(response.text)
