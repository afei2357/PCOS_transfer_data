from flask import Flask
from flask import jsonify,request
import requests
from config import Config
import base64

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

    
# 1 、GetLisRequest  接口（获取标本信息） ok
'''
1 、GetLisRequest  接口（获取标本信息）
LIS 将核收到的病人信息和医嘱信息，第三方外送检验机构通过“条码号”【参数：医院
条码】从该接口获取 LIS 的病人信息和医嘱信息（XML 文档字符串)
'''
@app.route("/GetLisRequest") #ok
def GetLisRequest():
    print('get a data from hospital  with api of GetLisRequest')
    #requests.get('192.168.1.202:8000')
    # data = '<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><GetLisRequest xmlns="http://tempuri.org/"><hospSampleID>3542646409</hospSampleID></GetLisRequest></soap12:Body></soap12:Envelope>'

    # data = '<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><GetLisRequest xmlns="http://tempuri.org/"><hospSampleID>42936757</hospSampleID></GetLisRequest></soap12:Body></soap12:Envelope>'
    data = '<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><GetLisRequest xmlns="http://tempuri.org/"><hospSampleID>2343127051</hospSampleID></GetLisRequest></soap12:Body></soap12:Envelope>'
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
返回：

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><AffirmRequestResponse xmlns="http://tempuri.org/"><AffirmRequestResult /></AffirmRequestResponse></soap:Body></soap:Envelope>

'''
@app.route("/AffirmRequest")
def AffirmRequest():
    print('get a data from hospital  with api of GetLisRequest')
    #requests.get('192.168.1.202:8000')
    print('get a data from hospital  with api of GetLisRequest')
    #requests.get('192.168.1.202:8000')
    # data = '''3542646409 3142647053 2842645034 '''
    data = '<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><AffirmRequest xmlns="http://tempuri.org/"><hospSampleID>2343127051</hospSampleID></AffirmRequest></soap12:Body></soap12:Envelope>'
    encode_data = data.encode('utf-8')
    # print(data)
    headers = {"Host": "10.10.11.196",
            "Content-Type": "application/soap+xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)),
            "SOAPAction": "http://tempuri.org/AffirmRequest"}
    #patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/test', data=encode_data,headers=headers)
    patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/ExtReportService', data=encode_data ,headers=headers)

    print('patient_info.header----')
    print(patient_info.headers)
    print('patient_info.text----')    
    print(patient_info.text)

    return patient_info.text,200#,ret_header


#3 、AffirmRequestWithExtBarc ok 
'''
3 、AffirmRequestWithExtBarcode  接口（确认获取标
本信息成功，回传 第三方外送检验机构 条码）
第三方外送检验机构通过 GetLisRequest 接口成功获取病人信息和医嘱信息后，通过
AffirmRequestWithExtBarcode 接口发送确认获取成功的信息，参数：医院条码，第三方条码
调用方式：AffirmRequest(HospSampleID,extBarcode)
返回结果：

<?xml version="1.0" encoding="utf-8"?><soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema"><soap:Body><AffirmRequestWithExtBarcodeResponse xmlns="http://tempuri.org/"><AffirmRequestWithExtBarcodeResult>&lt;response&gt;&lt;resultcode&gt;1&lt;/resultcode&gt;&lt;errormsg&gt;&lt;/errormsg&gt;&lt;/response&gt;</AffirmRequestWithExtBarcodeResult></AffirmRequestWithExtBarcodeResponse></soap:Body></soap:Envelope>

解码后：
<response><resultcode>1</resultcode><errormsg></errormsg></response>
'''
@app.route("/AffirmRequestWithExtBarcode") #ok
def AffirmRequestWithExtBarcode():
    print('get a data from hospital  with api of GetLisRequest')
    #requests.get('192.168.1.202:8000')
    # data = '''<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><GetLisItems xmlns="http://tempuri.org/" /></soap12:Body>/soap12:Envelope>'''
    data = '<?xml version="1.0" encoding="utf-8"?><soap12:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap12="http://www.w3.org/2003/05/soap-envelope"><soap12:Body><AffirmRequestWithExtBarcode xmlns="http://tempuri.org/"><hospSampleID>3542646409</hospSampleID><extBarcode>test_extBarcode</extBarcode></AffirmRequestWithExtBarcode></soap12:Body></soap12:Envelope>'
    encode_data = data.encode('utf-8')
    # print(data)
    headers = {"Host": "10.10.11.196",
            "Content-Type": "application/soap+xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)),
            "SOAPAction": "http://tempuri.org/AffirmRequestWithExtBarcode"}
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
    

    data1 = '''
<soap:Envelope
    xmlns:soap="http://www.w3.org/2003/05/soap-envelope"
    xmlns:tem="http://tempuri.org/">
    <soap:Header/>
    <soap:Body>
        <tem:UploadLisRepData>
            <!--Optional:-->
            <tem:reportResult>
                <![CDATA[<Report_Result><Report_Info><ext_lab_code></ext_lab_code><lis_Barcode>42936757</lis_Barcode><ext_Barcode>100311224212</ext_Barcode><ext_checkItem/><pat_name>测试0426</pat_name><pat_age/><pat_height/><pat_wight/><pat_pre_week/><pat_id>3722021823</pat_id><pat_bedNo/><pat_tel>10086</pat_tel><pat_sex/><pat_birthday/><pat_ori_name/><sam_name>血清</sam_name><sam_state/><doctor_name>郭佩湘</doctor_name><dept_name>1</dept_name><clinical_diag/><SampleNumber/><blood_time/><ext_check_ID/><ext_receive_time>2021-11-19 16:20:00</ext_receive_time><ext_upload_time/><ext_report_suggestion/><ext_report_remark/><ext_intstrmt_name/><ext_lab_name/><ext_report_type/><ext_check_time>2021-11-19 16:35:00</ext_check_time><ext_first_audit_time>2021-11-19 16:35:59</ext_first_audit_time><ext_second_audit_time>2021-11-19 16:35:59</ext_second_audit_time><ext_checker>黄孟孟</ext_checker><ext_first_audit>周紫燕</ext_first_audit><ext_second_audit>周紫燕</ext_second_audit><ext_report_code>1636961339000</ext_report_code><result_info><result_seq/><ext_combine_code>742</ext_combine_code><ext_combine_name>742</ext_combine_name><ext_item_code>742-9570</ext_item_code><ext_item_name>外院测试项目</ext_item_name><result>
                <![CDATA[6.4]]]]>>
                <![CDATA[</result><result_unit>
                <![CDATA[%]]]]>>
                <![CDATA[</result_unit><result_flag>
                <![CDATA[↓]]]]>>
                <![CDATA[</result_flag><result_reference>
                <![CDATA[7.4-12.6]]]]>>
                <![CDATA[</result_reference><result_date>2021-11-19 16:22:59</result_date><result_intstrmt_name/><result_test_method/><result_suggestion/><result_remark/><lis_combine_code>31798</lis_combine_code><lis_combine_name>院内测试组合</lis_combine_name><lis_item_code>32009</lis_item_code><lis_item_name>宫颈癌甲基化检测</lis_item_name></result_info><result_info><result_seq/><ext_combine_code>742</ext_combine_code><ext_combine_name>742</ext_combine_name><ext_item_code>742-9506</ext_item_code><ext_item_name>外院测试项目</ext_item_name><result>
                <![CDATA[35.6]]]]>>
                <![CDATA[</result><result_unit>
                <![CDATA[%]]]]>>
                <![CDATA[</result_unit><result_flag>
                <![CDATA[↑]]]]>>
                <![CDATA[</result_flag><result_reference>
                <![CDATA[8.0-15.8]]]]>>
                <![CDATA[</result_reference><result_date>2021-11-19 16:22:59</result_date><result_intstrmt_name/><result_test_method/><result_suggestion/><result_remark/><lis_combine_code>10983</lis_combine_code><lis_combine_name>院内测试组合</lis_combine_name><lis_item_code>32284</lis_item_code><lis_item_name>院内测试项目</lis_item_name></result_info><report_pic><pic_content>'''
                
    data3 = '''</pic_content><pic_name>test_base64.pdf</pic_name><pic_seq></pic_seq></report_pic></Report_Info></Report_Result>]]>
            </tem:reportResult>
        </tem:UploadLisRepData>
    </soap:Body>
</soap:Envelope>
    '''
    data2 = ''
    with open('test_base64.pdf','rb') as fh:
            data2 = base64.b64encode(fh.read())
    data = data1.encode('utf-8') + data2 + data3.encode('utf-8')
    # with open('1入参示例.xml',encoding="utf-8") as fh:

    # with open('入参2-2.txt',encoding="utf-8") as fh:
        # data = fh.read()

    
    # data = data1 + raw_data + data2
#encode_data = data.encode('utf-8')
    encode_data = data
    # print(data)
    headers = {"Host": "10.10.11.196",
            "Content-Type": "text/xml; charset=utf-8",
            # "Content-Type": "application/soap+xml; charset=UTF-8",  
            "Content-Length": str(len(encode_data)) ,#}
            "SOAPAction": "http://tempuri.org/UploadLisRepData"}
    #patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/test', data=encode_data,headers=headers)
    patient_info = requests.post(f'http://{Config.MIDDLE_HOST_ADDRESS}/ExtReportService', data=encode_data ,headers=headers)

    print('patient_info.header----')
    print(patient_info.headers)
    print('patient_info.text----')    
    print(patient_info.text)

    return patient_info.text,200#,ret_header 


@app.route("/UploadLisRepData2")
def UploadLisRepData2():
    print('get a data from hospital  with api of GetLisRequest')

 
    data = '''xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/"xmlns:tem="http://tempuri.org/"><soapenv:Header/><soapenv:Body><tem:UploadLisRepData><!--Optional:--><tem:reportResult><![CDATA[ <Report_Result><Report_Info><ext_lab_code></ext_lab_code><lis_Barcode>2442503307</lis_Barcode><ext_Barcode></ext_Barcode><ext_checkItem /><pat_name>李叶莲</pat_name><pat_age>52</pat_age><pat_height /><pat_wight /><pat_pre_week /><pat_id>2001696944</pat_id><pat_bedNo>None</pat_bedNo><pat_tel>13527706634</pat_tel><pat_sex>女</pat_sex><pat_birthday /><pat_ori_name>门诊</pat_ori_name><sam_name>默认</sam_name><sam_state /><doctor_name>王三锋</doctor_name><dept_name>妇科门诊(越秀)</dept_name><clinical_diag>[西]宫颈上皮内肿瘤，Ⅰ级</clinical_diag><SampleNumber>None</SampleNumber><blood_time>2022-03-11 01:24:09</blood_time><ext_check_ID /><ext_receive_time>2022-03-11 01:24:09</ext_receive_time><ext_upload_time /><ext_report_suggestion></ext_report_suggestion><ext_report_remark></ext_report_remark><ext_intstrmt_name /><ext_lab_name /><ext_report_type></ext_report_type><ext_check_time></ext_check_time><ext_first_audit_time></ext_first_audit_time><ext_second_audit_time></ext_second_audit_time><ext_checker></ext_checker><ext_first_audit></ext_first_audit><ext_second_audit></ext_second_audit><ext_report_code></ext_report_code><result_info><result_seq/><ext_combine_code /><ext_combine_name /><ext_item_code /><ext_item_name /><result><![CDATA[阴]]]]>><![CDATA[</result><result_unit></result_unit><result_flag></result_flag><result_reference></result_reference><result_date></result_date><result_intstrmt_name></result_intstrmt_name><result_test_method></result_test_method><result_suggestion></result_suggestion><result_remark></result_remark><lis_combine_code></lis_combine_code><lis_combine_name></lis_combine_name><lis_item_code></lis_item_code><lis_item_name></lis_item_name></result_info><report_pic><pic_name></pic_name><pic_seq></pic_seq></report_pic></Report_Info></Report_Result>]]></tem:reportResult></tem:UploadLisRepData></soapenv:Body></soapenv:Envelope>'''
    data = '''<soap:Envelopexmlns:soap="http://www.w3.org/2003/05/soap-envelope"xmlns:tem="http://tempuri.org/"><soap:Header/><soap:Body><tem:UploadLisRepData><!--Optional:--><tem:reportResult><![CDATA[<soap:Envelopexmlns:soap="http://www.w3.org/2003/05/soap-envelope"xmlns:tem="http://tempuri.org/"><soap:Header/><soap:Body><tem:UploadLisRepData><!--Optional:--><tem:reportResult><![CDATA[<Report_Result><Report_Info><ext_lab_code>42625453</ext_lab_code><lis_Barcode>42625453</lis_Barcode><ext_Barcode></ext_Barcode><ext_checkItem /><pat_name>测试0321</pat_name><pat_age>None</pat_age><pat_height /><pat_wight /><pat_pre_week /><pat_id>3013097142</pat_id><pat_bedNo>None</pat_bedNo><pat_tel>None</pat_tel><pat_sex>男</pat_sex><pat_birthday /><pat_ori_name>住院</pat_ori_name><sam_name>None</sam_name><sam_state /><doctor_name>曾志生</doctor_name><dept_name>测试</dept_name><clinical_diag>None</clinical_diag><SampleNumber>None</SampleNumber><blood_time>2022-03-21 09:00:25</blood_time><ext_check_ID /><ext_receive_time>2022-03-21 09:00:25</ext_receive_time><ext_upload_time /><ext_report_suggestion>受检者标本宫颈癌基因甲基化检测结果为阳性，请结合临床综合分析。</ext_report_suggestion><ext_report_remark></ext_report_remark><ext_intstrmt_name /><ext_lab_name /><ext_report_type>A4</ext_report_type><ext_check_time>2022-03-20 16:00:00</ext_check_time><ext_first_audit_time>2022-03-20 16:00:00</ext_first_audit_time><ext_second_audit_time>2022-03-20 16:00:00</ext_second_audit_time><ext_checker>张纪斌</ext_checker><ext_first_audit>毛荣丽</ext_first_audit><ext_second_audit>毛荣丽</ext_second_audit><ext_report_code>A4</ext_report_code><result_info><result_seq/><ext_combine_code /><ext_combine_name /><ext_item_code /><ext_item_name /><result><![CDATA[阳]]]]]]>><![CDATA[><![CDATA[</result><result_unit><![CDATA[Ct]]]]]]>><![CDATA[><![CDATA[</result_unit><result_flag></result_flag><result_reference></result_reference><result_date>2022-03-20 16:00:00</result_date><result_intstrmt_name>ABI 7500</result_intstrmt_name><result_test_method>qPCR</result_test_method><result_suggestion>受检者标本宫颈癌基因甲基化检测结果为阳性，请结合临床综合分析。</result_suggestion><result_remark></result_remark><lis_combine_code>32009</lis_combine_code><lis_combine_name>宫颈癌甲基化检测</lis_combine_name><lis_item_code>32344</lis_item_code><lis_item_name>外送项目</lis_item_name></result_info><report_pic><pic_content></pic_content><pic_name>宫颈癌基因甲基化检测报告-测试0321_Psl57i2.pdf</pic_name><pic_seq>1</pic_seq></report_pic></Report_Info></Report_Result> ]]]]>><![CDATA[</tem:reportResult></tem:UploadLisRepData></soap:Body></soap:Envelope>]]></tem:reportResult></tem:UploadLisRepData></soap:Body></soap:Envelope>'''
    encode_data = data.encode('utf-8')
    # print(data)
    headers = {"Host": "10.10.11.196",
            "Content-Type": "text/xml; charset=UTF-8",
            "Content-Length": str(len(encode_data)) ,#}
            "SOAPAction": "http://tempuri.org/UploadLisRepData"}
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
