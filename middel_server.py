from flask import Flask
from flask import jsonify,request
import requests
from config import Config
from extensions import logger 


app = Flask(__name__)

# 1 、GetLisRequest  接口（获取标本信息）
'''
1 、GetLisRequest  接口（获取标本信息）
LIS 将核收到的病人信息和医嘱信息，第三方外送检验机构通过“条码号”【参数：医院
条码】从该接口获取 LIS 的病人信息和医嘱信息（XML 文档字符串)
'''
@app.route("/ExtReportService",methods=['POST'])
def ExtReportService():
    ip = request.remote_addr
    #logger.info(ip)
#    if ip == f'{Config.REMOTE_SERVER_ADDRESS}'.split(':')[0]:
    logger.info('get a connection ip is :'+ip)
    print('get a connection ip is :'+ip)
    #logger.info(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) )
#    print(request.data)
    #response.encoding = 'gb2312'
    request_patient_info = requests.post(f'http://{Config.LOCAL_HOST_ADDRESS}/ExtReportService.asmx',data=request.data,headers=request.headers)
    print(request.headers)
    request_patient_info.encoding = 'utf-8'
    logger.info(request_patient_info.text)
    print(request_patient_info.text)
    logger.info(request_patient_info.headers)
    return request_patient_info.text


@app.route("/ExtReportService2",methods=['POST'])
def ExtReportService2():
    ip = request.remote_addr
    #logger.info(ip)
#    if ip == f'{Config.REMOTE_SERVER_ADDRESS}'.split(':')[0]:
    logger.info('get a connection ip is :'+ip)
    print('get a connection ip is :'+ip)
    #logger.info(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) )
#    print(request.data)
    #response.encoding = 'gb2312'
    request_patient_info = requests.post(f'http://{Config.LOCAL_HOST_ADDRESS}/ExtReportService.asmx',data=request.data,headers=request.headers)
    print(request.headers)
    request_patient_info.encoding = 'utf-8'
    logger.info(request_patient_info.text)
    print(request_patient_info.text)
    logger.info(request_patient_info.headers)
    return request_patient_info.text


# 1 、GetLisRequest  接口（获取标本信息）
'''
1 、GetLisRequest  接口（获取标本信息）
LIS 将核收到的病人信息和医嘱信息，第三方外送检验机构通过“条码号”【参数：医院
条码】从该接口获取 LIS 的病人信息和医嘱信息（XML 文档字符串)
'''
@app.route("/GetLisRequest",methods=['POST'])
def GetLisRequest():
    ip = request.remote_addr
    #logger.info(ip)
#    if ip == f'{Config.REMOTE_SERVER_ADDRESS}'.split(':')[0]:
    logger.info('get a connection ip is :'+ip)
    #logger.info(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) )
#    print(request.data)
    request_patient_info = requests.post(f'http://{Config.LOCAL_HOST_ADDRESS}/GetLisRequest',data=request.data,headers=request.headers)
#request_patient_info = requests.post(f'http://{ip}/GetLisRequest',data=request.data,headers=request.headers)
    print(request_patient_info.text)
    print(request_patient_info.headers)
    return request_patient_info.text

'''
# 2 、AffirmRequest  接口（确认获取标本信息成功）
# 第三方外送检验机构通过 GetLisRequest 接口成功获取病人信息和医嘱信息后，通过
AffirmRequest 接口发送确认获取成功的信息，参数：医院条码
调用方式：AffirmRequest(HospSampleID)
'''
@app.route("/AffirmRequest",methods=['POST'])
def AffirmRequest():
    ip = request.remote_addr
    logger.info('get a connection ip is :'+ip)
    print(request.data)
    AffirmRequest_info = requests.post(f'http://{Config.LOCAL_HOST_ADDRESS}/AffirmRequest',data=request.data,headers=request.headers)
    return AffirmRequest_info.text

#3 、AffirmRequestWithExtBarc
'''
3 、AffirmRequestWithExtBarcode  接口（确认获取标
本信息成功，回传 第三方外送检验机构 条码）
第三方外送检验机构通过 GetLisRequest 接口成功获取病人信息和医嘱信息后，通过
AffirmRequestWithExtBarcode 接口发送确认获取成功的信息，参数：医院条码，第三方条码
调用方式：AffirmRequest(HospSampleID,extBarcode)
'''
@app.route("/AffirmRequestWithExtBarcode",methods=['POST'])
def AffirmRequestWithExtBarcode():
    ip = request.remote_addr
    logger.info('get a connection ip is :'+ip)
    print(AffirmRequest_info.text)
    print(request.data)
    AffirmRequest_info = requests.post(f'http://{Config.LOCAL_HOST_ADDRESS}/AffirmRequestWithExtBarcode',data=request.data,header=request.headers)
    return AffirmRequest_info.text


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
    ip = request.remote_addr
    logger.info('get a connection ip is :'+ip)
    print(AffirmRequest_info.text)
    UploadLisRepDataRequest_info = requests.post(f'http://{Config.LOCAL_HOST_ADDRESS}/UploadLisRepData',data=request.data,header=request.headers)
#    print(UploadLisRepDataRequest_info.text)
    return UploadLisRepDataRequest_info.text

@app.route("/t2")
def hello_world():
    print('get a data ')
    #requests.get('192.168.1.202:8000')
    print(request.args)
    print(request.data)
    print(request.headers)
    print(request.get_data())
    return "<p>Hello, World! t2 </p>"

@app.route("/host2server",methods=['POST'])
def host2server():
    ip = request.remote_addr
    print('get a local connect,ip is: '+ip)
    #if ip == f'{Config.LOCAL_HOST_ADDRESS}'.split(':')[0]:
#logger.info(id)
    #print(request.data.decode('utf-8'))
    headers={
          "content-type": "text/xml; charset=utf-8"
    }
    #requests.post(f'http://{Config.REMOTE_SERVER_ADDRESS}/send2server',data=request.data.encode('utf-8'),headers=headers)
    requests.post(f'http://{Config.REMOTE_SERVER_ADDRESS}/send2server',data=request.data,headers=headers)
    return "<p>the middle server get a connect, host2server, the ip is :</p>"+ ip

@app.route("/server2host",methods=['POST'])
def server2host():
    ip = request.remote_addr
    print('get a remote connect,ip is: '+ip)
    #if ip == f'{Config.REMOTE_SERVER_ADDRESS}'.split(':')[0]:
    #print(request.data.decode('utf-8'))
#logger.info(ip)
    headers={
          "content-type": "text/xml; charset=utf-8"
    }
    #logger.info(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) )
    #requests.post(f'http://{Config.LOCAL_HOST_ADDRESS}/send2host',data=request.data,headers=headers)
    requests.post(f'http://{Config.LOCAL_HOST_ADDRESS}/send2host',data=request.data)
    return "<p>the middle server get a connect, send2host, the ip is :</p>"+ ip


def configure_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')

# waitress-serve --host=0.0.0.0 --port=4431 middel_server:app
if __name__ == '__main__':
    app.run(port=4431,host='0.0.0.0',debug=True)


