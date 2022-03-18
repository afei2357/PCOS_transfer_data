from flask import Flask
from flask import jsonify,request
import requests
from config import Config

#if ip == '' and post_secret = 'i_am_server': 

#模拟远程云服务器的环境
app = Flask(__name__)

@app.route("/t3")
def hello_world():
    print('get a data ')
    #requests.get('192.168.1.202:8000')
    print(request.args)
    print(request.data)
    print(request.get_data())
    return "<p>Hello, World! t2 </p>"

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
    data = '''
    <?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <GetLisRequest xmlns="http://tempuri.org/">
      <hospSampleID>string</hospSampleID>
    </GetLisRequest>
  </soap12:Body>
</soap12:Envelope>
    '''
    encode_data = data.encode('utf-8')
    print(data)
    headers = {"Host": "10.10.11.196",
            "Content-Type": "application/soap+xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)),
            "SOAPAction": "http://tempuri.org/AffirmRequest"}
    patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/GetLisRequest', data=encode_data,headers=headers)
    print('patient_info.text----')
    print(patient_info.headers)
    ret_header = patient_info.headers
    ret_header.pop('Date')
    ret_header.pop('Server')
    print(ret_header)
    return patient_info.text,200#,ret_header
'''
# 2 、AffirmRequest  接口（确认获取标本信息成功）
# 第三方外送检验机构通过 GetLisRequest 接口成功获取病人信息和医嘱信息后，通过
AffirmRequest 接口发送确认获取成功的信息，参数：医院条码
调用方式：AffirmRequest(HospSampleID)
'''
@app.route("/AffirmRequest")
def AffirmRequest():
    print('get a data from hospital  with api of GetLisRequest')
    #requests.get('192.168.1.202:8000')
    print('1request.args-------')
    print(request.args.get('HospSampleID'))
    data = '''
    <?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <AffirmRequest xmlns="http://tempuri.org/">
      <hospSampleID>string</hospSampleID>
    </AffirmRequest>
  </soap12:Body>
</soap12:Envelope>
    '''
    encode_data = data.encode('utf-8')
    headers = {"Content-Type": "application/soap+xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)),
            }
    AffirmRequest_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/AffirmRequest', data=encode_data,headers=headers)
    return AffirmRequest_info.text


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
    print('get a data from hospital  with api of GetLisRequest')
    #requests.get('192.168.1.202:8000')
    print('1request.args-------')
    print(request.args.get('HospSampleID'))
    data = '''
    <?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <AffirmRequestWithExtBarcodeResponse xmlns="http://tempuri.org/">
      <AffirmRequestWithExtBarcodeResult>string</AffirmRequestWithExtBarcodeResult>
    </AffirmRequestWithExtBarcodeResponse>
  </soap12:Body>
</soap12:Envelope>
    '''
    encode_data = data.encode('utf-8')
    headers = {"Content-Type": "application/soap+xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)),
            }
    return encode_data,200,headers 
    AffirmRequest_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/server2host_AffirmRequestWithExtBarcode', data=encode_data)
    return AffirmRequest_info.text


'''
4 、UploadLisRepData  接口（回传结果和报告单）
第三方外送检验机构通过 UploadLisRepData 接口回传项目检验结果和报告单，参数：
XML 文档字符串
<!--回传结果是以报告单为单位回传，有多张报告单时，我们回传多次，各次的区别是
以“报告单号”来区分-->
调用方式：UploadLisRepData(ResultXML)
'''
@app.route("/UploadLisRepData")
def UploadLisRepData():
    with open('test.xml',encoding='utf-8') as fh:
        tree = fh.read()
    UploadLisRepDataRequest_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/server2host_UploadLisRepData', data=tree.encode('utf-8'))
    data = '''
    <?xml version="1.0" encoding="utf-8"?>
<soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope">
  <soap12:Body>
    <UploadLisRepData xmlns="http://tempuri.org/">
      <reportResult>string</reportResult>
    </UploadLisRepData>
  </soap12:Body>
</soap12:Envelope>
    '''
    encode_data = data.encode('utf-8')
    headers = {"Content-Type": "application/soap+xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)),
            }
    return encode_data,200,headers 
    return UploadLisRepDataRequest_info.text
#return "<p>server2host!</p>"

@app.route("/send2server",methods=['POST'])
def send2server():
    print('request.data -----1')
    print(request.data.decode('utf-8'))
    print('request.get_data() -----2')
    #print(request.get_data())
    print('request.values -----3')
    #print(request.values)
    #requests.post('192.168.1.202:8000')
    ip = request.remote_addr
    print('the id is : ------4')
    print(id)
    print(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) )
    return "<p>Hello, World! t33 </p>"

@app.route("/test_server2host")
def test_server2host():
    with open('test.xml') as fh:
        tree = fh.read()
    headers={
          "content-type": "text/xml; charset=utf-8"
    }
    requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/server2host', data=tree.encode('utf-8'),headers=headers)
    return "<p>server2host!</p>"

if __name__ == '__main__':
    app.run(port=8003,host='0.0.0.0',debug=True)
