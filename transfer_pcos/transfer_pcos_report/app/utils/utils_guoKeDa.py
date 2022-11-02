import json
import base64
import requests as rq
from html.parser import HTMLParser
import requests,base64,os,zipfile
from xml.etree import ElementTree  as ET
#from app.models.models_pcos import Reports 
#from app import db
from datetime import datetime




# 获取信息接口
def get_patient_infos(barcode):
    data = f'<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tem="http://tempuri.org/"><soapenv:Header/><soapenv:Body><tem:LisMainInterface><tem:methodName>PATIENTINFO</tem:methodName><tem:inParam>{{"barcode":"{barcode}"}}</tem:inParam><tem:paramType>1</tem:paramType></tem:LisMainInterface></soapenv:Body></soapenv:Envelope>'
    # encode_data = data.encode('utf-8')
    encode_data = data
    headers = {"Content-Length": str(len(encode_data)),"Accept-Encoding":"gzip,deflate",'Content-Type':'text/xml;charset=UTF-8','SOAPActiom':"http://tempuri.org/LisMainInterface",'Host':'weixin.ucasszh.cn:8007','User-Agent':'Apache-HttpClient/4.1.1 (java 1.5)'}
    ret = rq.post('https://weixin.ucasszh.cn:8007/Interface/LisOnlineInterface.asmx?wsdl',data=data,headers=headers)
    return ret

# 从一个ini配置文件里，拿到变量映射的关系，返回字典形式的映射关系
def parser_config_to_json(f_ini ):
    from collections import defaultdict
    try:
        import ConfigParser as configparser
    except ModuleNotFoundError:
        import configparser
    config = defaultdict(dict)
    cf = configparser.ConfigParser()
    cf.read(f_ini)
    sections = cf.sections()
    for section in sections:
        options = cf.options(section)
        for option in options:
             if option in config[section]:
                 sys.stderr.write(( 'duplication option:{} of section:{} in '
                                    'config:{}').format(option, section, f_ini))
                 sys.exit(1)
             tmp = cf.get(section, option)
             if tmp:
                 # assert os.path.exists(tmp), \
                 #     'option:{} of section:{} is not exists! '.format(option, section)
                 config[section][option] = tmp
    return config

# 根据映射关系，将某个字典里的key转为映射后的新key,其中hospital_name是配制文件里的键，
def change_dct_key(hospital_name,config,old_dct):
    new_dct = {}
    for key1,value1 in old_dct.items():
        if not config[hospital_name].get(key1) :
            # 如果发来的数据中的key不在 配置文件里，就跳过这个key
            print('the key is not in the config mapping: '+ key1)
            continue 
        new_dct[config[hospital_name].get(key1)] = value1
        # 对字典里的数组做循环，把数组里的多个字典里的key映射成新的key
        if type(value1)==list :
            new_dct[config[hospital_name].get(key1)] = []
            for dct in value1:
                inner_dct = {}
                for key2,value2 in dct.items():
                    inner_dct[config[ hospital_name].get(key2) ] = value2
                new_dct[ config[hospital_name].get(key1) ].append(inner_dct )
    return new_dct

#if __name__ == '__main__':
def test_change_config():
    #{'a': 'aa', 'b': 'bbBB', 'testid': 'test_id'}
    aa = '4a'
    bbBB = '4b'
    test_id= 'test_idtest_id'
    old_dct = {'test':"ttt",'lab_name':"爱湾",'test_order_product_sample_no':"样本编码",'checker_name':'实验员','test_product_samples':[{'sample_id':'id1'},{'sample_id':'id2'}]}
    old_dct = {
 "lab_name": "爱湾", 
 "barcode": "123456", 
 "experiment_no": "65321", 
 "test_order_product_sample_no": "sample_code123", 
 "inspector": "test_name", 
 "inspection_time": "2012-11-01 10:35:10", 
 "checker_name": "check_name", 
 "check_time": "2012-11-01 10:35:10", 
 "test_product_remark": "backup", 
 "test_product_pdf_content": "pdf_content", 
 "test_product_pdf_name": 'test_product_pdf_name', 
 "test_product_pdf_no": 'test_product_pdf_no', 
 "test_product_samples": [
  {
   "sample_id": 'sample_id', 
   "sample_name": 'sample_name', 
   "sample_result": 'sample_result', 
   "sample_unit": 'sample_unit', 
   "sample_contrast_flag": 'sample_contrast_flag', 
   "sample_refrence": 'sample_refrence', 
   "test_method_name": 'test_method_name', 
  },
 {
   "sample_id": 'sample_id2', 
   "sample_name": 'sample_name2', 
   "sample_result": 'sample_result2', 
   "sample_unit": 'sample_unit2', 
   "sample_contrast_flag": 'sample_contrast_flag2', 
   "sample_refrence": 'sample_refrence2', 
   "test_method_name": 'test_method_name2', 
  },
  
 ], 
}

    config_ini_file  = 'mapping.txt'
    hospital_name  = 'guoKeDa'
    config = parser_config_to_json(config_ini_file )
    new_dct = change_dct_key(hospital_name,config,old_dct)

    #print(config['guoKeDa'])
    print(new_dct)
    print('old_dct---')
    print(old_dct)
    #print(eval(config['abc']['a']))
if __name__ == '__main__':
    test_change_config()
    #get_patient_info('20255295401')
