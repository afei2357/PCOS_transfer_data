import requests as rq
import json,time

file = 'test_remote_json.json'
j = ''
with open(file,'r' ) as  fh:
    j = fh.read()
#headers = {'Content-Type': 'application/json'}
data = j.encode('utf-8')

barcode_lst = ["2022021701","202200301","202200701","20221401","20222101","20222102","20222102","2022032801","2022032801","2022032901","2022032901","2022040801","20104356501","20113328101","20113328001","2022050201","2022050202","20134683101","20142430501","20142430601","20145807701","20151523301","20151523501","20156201801","20158132601","20164841901","20164841801","220164966501","20168370101","20168370201","20165818001"]

#ret = rq.post('http://1.14.160.227:7000/send_result',data=j,headers=headers)
#ret = rq.post('http://1.14.160.227:7000/api/send_report',data=data)
for barcode in barcode_lst:
    ret = rq.get(f'http://1.14.160.227:7000/api/get_patient_info?barcode={barcode}')
    #print(ret.text)
    print('--------ret.text=====')
    print(barcode,json.loads(ret.text)['resultMsg'])
    time.sleep(2)
