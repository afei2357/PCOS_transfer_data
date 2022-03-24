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

# 0 test
@app.route("/ExtReportService")
def ExtReportService():
    print('get a data from hospital  with api of GetLisRequest')
    #requests.get('192.168.1.202:8000')
    # data = '''<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><GetLisItems xmlns="http://tempuri.org/" /></soap12:Body>/soap12:Envelope>'''
    data = '<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><GetLisRequest xmlns="http://tempuri.org/"><hospSampleID>3142647053</hospSampleID></GetLisRequest></soap12:Body></soap12:Envelope>'
    encode_data = data.encode('utf-8')
    # print(data)
    headers = {"Host": "10.10.11.196",
            "Content-Type": "application/soap+xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)),
            "SOAPAction": "http://tempuri.org/GetLisRequest"}
    #patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/test', data=encode_data,headers=headers)
    patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/ExtReportService', data=encode_data ,headers=headers)

    print('patient_info.header----')
    print(patient_info.headers)
    print('patient_info.text----')    
    print(patient_info.text)

    return patient_info.text,200#,ret_header

    

@app.route("/test")
def test():
    print('get a data from hospital  with api of GetLisRequest')
    #requests.get('192.168.1.202:8000')
    data = '''<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><GetLisItems xmlns="http://tempuri.org/" /></soap12:Body>/soap12:Envelope>'''
    encode_data = data.encode('utf-8')
    # print(data)
    headers = {"Host": "10.10.11.196",
            "Content-Type": "application/soap+xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)),
            "SOAPAction": "http://tempuri.org/AffirmRequest"}
    #patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/test', data=encode_data,headers=headers)
    patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/test', data=encode_data ,headers=headers)

    print('patient_info.header----')
    print(patient_info.headers)
    print('patient_info.text----')    
    print(patient_info.text)

    # ret_header = patient_info.headers
    # ret_header.pop('Date')
    #ret_header.pop('Server')
    # print(ret_header)
    # return 'aaaaa'
    return patient_info.text,200#,ret_header

    
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
    # data = '''<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><GetLisItems xmlns="http://tempuri.org/" /></soap12:Body>/soap12:Envelope>'''
    data = '<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><GetLisRequest xmlns="http://tempuri.org/"><hospSampleID>3142647053</hospSampleID></GetLisRequest></soap12:Body></soap12:Envelope>'
    encode_data = data.encode('utf-8')
    # print(data)
    headers = {"Host": "10.10.11.196",
            "Content-Type": "application/soap+xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)),
            "SOAPAction": "http://tempuri.org/GetLisRequest"}
    #patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/test', data=encode_data,headers=headers)
    patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/ExtReportService', data=encode_data ,headers=headers)

    print('patient_info.header----')
    print(patient_info.headers)
    print('patient_info.text----')    
    print(patient_info.text)

    return patient_info.text,200#,ret_header


'''
# 2 、AffirmRequest  接口（确认获取标本信息成功）
# 第三方外送检验机构通过 GetLisRequest 接口成功获取病人信息和医嘱信息后，通过
AffirmRequest 接口发送确认获取成功的信息，参数：医院条码
调用方式：AffirmRequest(HospSampleID)
返回乱码： 
æå¡å¨æ æ³ä¸ºè¯·æ±æä¾æå¡ï¼å ä¸ºä¸æ¯æè¯¥åªä½ç±»åã
'''
@app.route("/AffirmRequest")
def AffirmRequest():
    print('get a data from hospital  with api of GetLisRequest')
    #requests.get('192.168.1.202:8000')
    print('get a data from hospital  with api of GetLisRequest')
    #requests.get('192.168.1.202:8000')
    # data = '''3542646409 3142647053 2842645034 '''
    data = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><AffirmRequest xmlns="http://tempuri.org/"><hospSampleID>3542646409</hospSampleID></AffirmRequest></soap:Body></soap:Envelope>'
    encode_data = data.encode('utf-8')
    # print(data)
    headers = {"Host": "10.10.11.196",
            "Content-Type": "application/soap+xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)),
            "SOAPAction": "http://tempuri.org/GetLisRequest"}
    #patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/test', data=encode_data,headers=headers)
    patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/ExtReportService', data=encode_data ,headers=headers)

    print('patient_info.header----')
    print(patient_info.headers)
    print('patient_info.text----')    
    print(patient_info.text)

    return patient_info.text,200#,ret_header


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
    # data = '''<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><GetLisItems xmlns="http://tempuri.org/" /></soap12:Body>/soap12:Envelope>'''
    data = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><AffirmRequestWithExtBarcode xmlns="http://tempuri.org/"><hospSampleID>3542646409</hospSampleID><extBarcode>test_extBarcode</extBarcode></AffirmRequestWithExtBarcode></soap:Body></soap:Envelope>'
    encode_data = data.encode('utf-8')
    # print(data)
    headers = {"Host": "10.10.11.196",
            "Content-Type": "application/soap+xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)),
            "SOAPAction": "http://tempuri.org/GetLisRequest"}
    #patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/test', data=encode_data,headers=headers)
    patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/ExtReportService', data=encode_data ,headers=headers)

    print('patient_info.header----')
    print(patient_info.headers)
    print('patient_info.text----')    
    print(patient_info.text)

    return patient_info.text,200#,ret_header


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
    print('get a data from hospital  with api of GetLisRequest')
    #requests.get('192.168.1.202:8000')
    # data = '''<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><GetLisItems xmlns="http://tempuri.org/" /></soap12:Body>/soap12:Envelope>'''
    data = '<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"><soap:Body><UploadLisRepData xmlns="http://tempuri.org/"><reportResult>reportResult_requests</reportResult></UploadLisRepData></soap:Body></soap:Envelope>'
    encode_data = data.encode('utf-8')
    # print(data)
    headers = {"Host": "10.10.11.196",
            "Content-Type": "application/soap+xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)),
            "SOAPAction": "http://tempuri.org/GetLisRequest"}
    #patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/test', data=encode_data,headers=headers)
    patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/ExtReportService', data=encode_data ,headers=headers)

    print('patient_info.header----')
    print(patient_info.headers)
    print('patient_info.text----')    
    print(patient_info.text)

    return patient_info.text,200#,ret_header

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
