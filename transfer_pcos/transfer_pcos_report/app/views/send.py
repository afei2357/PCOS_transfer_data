import requests as rq
import json

file = 'test_remote_json.json'
j = ''
with open(file,'r' ) as  fh:
    j = fh.read()
#headers = {'Content-Type': 'application/json'}
data = j.encode('utf-8')

#ret = rq.post('http://1.14.160.227:7000/send_result',data=j,headers=headers)
#ret = rq.post('http://1.14.160.227:7000/api/send_report',data=data)
ret = rq.get('http://1.14.160.227:7000/api/get_patient_info?barcode=20255295401')
print(ret.text)
