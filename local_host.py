from flask import Flask,request
import requests,json
import xml.etree.ElementTree as ET
app = Flask(__name__)
from config import Config

# 模拟医院内部的环境
@app.route("/t1")
def hello_world():
    requests.get(f'http://{Config.MIDDLE_HOST_ADDRESS}/t2', params={'q': 'python', 'cat': '1001'})
    return "<p>Hello, World!</p>"

@app.route("/t11")
def hello_world2():
    with open('test.xml',encoding='utf-8') as fh:
        tree = fh.read()
        print('-------')
    headers={
          "content-type": "text/xml; charset=utf-8"
    }
    requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/host2server', data=tree.encode('utf-8'),headers=headers)
    return "<p>Hello, World!</p>"

@app.route("/send2host",methods=['POST'])
def send2server():
    print('request.data -----1')
    print(request.data)
    print('request.get_data() -----2')
    print(request.get_data())
    print('request.values -----3')
    print(request.values)
    #requests.post('192.168.1.202:8000')
    ip = request.remote_addr
    print('the id is : ------4')
    print(id)
    print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) )
    return "<p>Hello, this is local_host.py ! t33 </p>"

if __name__ == '__main__':
    app.run(port=8001,host='0.0.0.0',debug=True)
