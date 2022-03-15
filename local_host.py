from flask import Flask,request
import requests,json
import xml.etree.ElementTree as ET
app = Flask(__name__)
from config import Config

# 1 、GetLisRequest  接口（获取标本信息）
'''
1 、GetLisRequest  接口（获取标本信息）
LIS 将核收到的病人信息和医嘱信息，第三方外送检验机构通过“条码号”【参数：医院
条码】从该接口获取 LIS 的病人信息和医嘱信息（XML 文档字符串)
'''
@app.route("/GetLisRequest")
def GetLisRequest():
    print('get a data from hospital  with api of GetLisRequest')
    #requests.get('192.168.1.202:8000')
    print('1request.args-------')
    print(request.args)
    with open('patient_info.xml',encoding='utf-8') as fh:
        patient = fh.read()
        print('patient info -------')
        print(patient)
    return patient

'''
# 2 、AffirmRequest  接口（确认获取标本信息成功）
# 第三方外送检验机构通过 GetLisRequest 接口成功获取病人信息和医嘱信息后，通过
AffirmRequest 接口发送确认获取成功的信息，参数：医院条码
调用方式：AffirmRequest(HospSampleID)
'''
@app.route("/AffirmRequest")
def AffirmRequest():
    print('get a data from hospital  with api of AffirmRequest')
    #requests.get('192.168.1.202:8000')
    print('1request.args-------')
    print(request.args)
    return 'this is local host ,finish AffirmRequest '

#3 、AffirmRequestWithExtBarc
'''
3 、AffirmRequestWithExtBarcode  接口（确认获取标
本信息成功，回传 第三方外送检验机构 条码）
第三方外送检验机构通过 GetLisRequest 接口成功获取病人信息和医嘱信息后，通过
AffirmRequestWithExtBarcode 接口发送确认获取成功的信息，参数：医院条码，第三方条码
调用方式：AffirmRequest(HospSampleID,extBarcode)
'''
@app.route("/AffirmRequestWithExtBarcode")
def AffirmRequestWithExtBarcode():
    print('get a data from hospital  with api of AffirmRequest')
    #requests.get('192.168.1.202:8000')
    print('1request.args-------')
    print(request.args)
    return 'this is local host ,finish server2host_AffirmRequestWithExtBarcode '
# 模拟医院内部的环境

'''
4 、UploadLisRepData  接口（回传结果和报告单）
第三方外送检验机构通过 UploadLisRepData 接口回传项目检验结果和报告单，参数：
XML 文档字符串
<!--回传结果是以报告单为单位回传，有多张报告单时，我们回传多次，各次的区别是
以“报告单号”来区分-->
调用方式：UploadLisRepData(ResultXML)
'''
@app.route("/UploadLisRepData",methods=['POST'])
def UploadLisRepData():
    print('get a data from hospital  with api of UploadLisRepData')
    #requests.get('192.168.1.202:8000')
    print('1request.args-------')
    print(request.data.decode('utf-8'))
    return 'this is local host ,finish UploadLisRepData '

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
    print(request.data.decode('utf-8'))
    #print('request.get_data() -----2')
    #print(request.get_data())
    #print('request.values -----3')
    #print(request.values)
    #requests.post('192.168.1.202:8000')
    ip = request.remote_addr
    print('the id is : ------4')
    print(id)
    print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) )
    return "<p>Hello, this is local_host.py ! t33 </p>"

if __name__ == '__main__':
    app.run(port=8001,host='0.0.0.0',debug=True)
