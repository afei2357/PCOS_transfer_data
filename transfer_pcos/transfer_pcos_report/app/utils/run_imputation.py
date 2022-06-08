#encoding:utf8
import json,os,stat,zipfile,glob
from datetime import datetime
#import pandas as pd
#import pysnooper
import argparse
import sys
import celery 
import subprocess as sp 
from flask_mail import Message,Mail
from collections import defaultdict

now_path  =  os.path.abspath( os.path.dirname(__file__))
sys_root = os.path.abspath(now_path + '/../..') 
sys.path.append(sys_root)
#sys.path.append('/ifs1/Reohealth/project/report_on_web/v2.0')
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except Exception as e:
    print(e)

# 下列函数，如果某个目录不存在，就创建这个目录
def if_not_exist_file_mkdir(fullpath):
    if not os.path.exists(fullpath):
         os.makedirs(fullpath)

#@celery.task(bind=True)
def run_all_shell_bk(self,project_dir,obj_dict,recipients):
    print('===============obj_dict==========------')
    print(obj_dict)

#from app import celery_logger
#@celery.task(bind=True)
def test(self):
    print('==============test_run_celery1==========------')
    #celery_logger.info('celery_log1-----------')
    #for i in range(10):
    #    celery_logger.info(i)
    #celery_logger.info('celery_log2-----------')
    print('==============test_run_celery2==========------')

#@celery.task(bind=True)
def run_all_shell(self,project_dir,obj_dict,recipients):
    from app import create_app
    start = datetime.now()
    app = create_app()
    filezip = project_dir + '/' + project_dir.split('/')[-1] + '_imputeResult.zip'
    with app.app_context(),zipfile.ZipFile(filezip,'w',zipfile.ZIP_DEFLATED) as zipfh:
        cwd = os.getcwd()
        #os.chdir(project_dir)
        info = '以下内容是impute的结果概况:</p>'
        #for sample in obj_dict.get('all_sample'):
        for sample_path in obj_dict.get('all_sample_path'):
            #sample_dir = os.path.join(project_dir,sample)     
            shell_file = os.path.join(sample_path,'impute.sh')
            Sample_product_dir = '_'.join(sample_path.split('/')[-2:])
            print('========== shell_file1===========')
            print( shell_file)
            impute_result = ''
            if os.path.isfile(shell_file):
                # 修改为可执行权限
                os.chmod(shell_file, stat.S_IRWXU|stat.S_IRGRP|stat.S_IROTH)  
                print('========== run_shell 2===========')
                # 执行log.sh脚本：
                sp.call(shell_file)
                impute_result = f'{sample_path}/{Sample_product_dir}_rs_result.txt'
                remain_miss_rs = f'{sample_path}/{Sample_product_dir}_remain_miss_rs.txt'
            if os.path.exists(impute_result):
                info = info + Sample_product_dir + ': 完成 '
                impute_result_name = impute_result.split('/')[-1]
                #zipfh.write(impute_result,impute_result_name)
                if os.path.exists(remain_miss_rs):
                    remain_miss_rs_name = remain_miss_rs.split('/')[-1]
                    zipfh.write(remain_miss_rs,remain_miss_rs_name)
                    rs_miss_lst = []
                    with open(remain_miss_rs) as miss_fh:
                        for line in miss_fh:
                            line = line.strip()
                            rs_miss_lst.append(line)
                    info = info + ' ,但仍缺少位点,请手动补充再运行报告 : ' + ','.join(rs_miss_lst)
                info = info +  ' ; </p>'
            else:
                info = info + Sample_product_dir + f': 失败 ; </p>'
        # 合并相同产品的结果：
        product_path_dict = get_product_result_path(project_dir)
        merge_result_path_lst = write_dict(project_dir,product_path_dict)
        [ zipfh.write(product_result_path,product_result_name) for (product_result_path,product_result_name) in merge_result_path_lst ]
        #zipfh.write(impute_result,impute_result_name)


        info = info +f'项目地址：{project_dir}</p></p>'
        all_spend_time = (datetime.now() - start).seconds
        minite,second = divmod(all_spend_time,60)
        hour,minite = divmod(minite,60)
        info = info +  f'总耗时： {hour}小时{minite}分钟</p></p>'
        #os.chdir(cwd)
        send_email(app,filezip,info,recipients)
        #print('after run and chdir ,the cwd is :\n'+os.getcwd())
        return  info
def get_product_result_path(project_dir):
    path_lst = glob.glob(os.path.join(project_dir,r'*/*/*rs_result.txt'))
    product_path_dict = defaultdict(list)
    for i in path_lst:    
        if i.endswith('_rs_result.txt'):
            print(i.split('_')[-3])
            product = i.split('_')[-3]
            product_path_dict[product].append(i)
    return product_path_dict



#send_file 是需要发送的文件的全路径
def send_email(app,send_file,info,recipients):
    mail = Mail(app)
    #msg = Message("impuation 结果",sender="huangzengfei@reohealth.cn",recipients=["afei2357@qq.com","zans2009@qq.com"])
    msg = Message("impuation 结果",sender="huangzengfei@reohealth.cn",recipients=recipients)
    msg.body = 'imputation 结果 '
    msg.html =f'<b> 你好<b></p> {info} </p>本邮件由系统自动发送,如有疑问请询问管理员.</p>祝好！'
    file_name = os.path.split(send_file)[-1]
    with app.open_resource(send_file) as fp:
        msg.attach(file_name,'application/x-bzip',fp.read())
    mail.send(msg)
    #return  '发送成功'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i' ,'--in_excel',help='请输入Excel文件，以生成run1.sh run2.sh 和配置文件')
    parser.add_argument('-o' ,'--out',help='输入的目录地址，默认本地目录')
    args = parser.parse_args()
    infile =  args.in_excel
    outdir = args.out or '.'
    if not infile:
        os.sys.exit('由于未输入 Excel文件作为参数，程序已经中断\n请用重新运行，用-e 参数来添加Excel文件。')

if __name__ == '__main__':
    main()
