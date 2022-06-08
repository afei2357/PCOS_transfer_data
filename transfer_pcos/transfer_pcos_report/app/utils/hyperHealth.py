##encoding:utf8
#import os,shutil
#import pandas as pd
#from pandas import DataFrame
#import datetime,random
#from flask import  Flask,jsonify,request,make_response,render_template,flash,redirect,url_for,abort,send_from_directory
#from app import  db
#from . import hyperHealthView
#from app.configs.config import basedir
#
#from app.utils.utils import read_xls,rename_df,if_not_exist_file_mkdir,compress
#from app.utils.utils import save_upload_file,run_shell
#
#basepath = os.path.join(basedir,'work_dir/HyperHealth')

from utils import save_snp_info_csv,save_upload_file
#replce_columns = ["sample_id","gender","age","height","weight","SBP","SBP_treated","DBP","current_smoker","parental_hypertension","diabetes","prior_CVD","AF","LVH","prior_stroke_or_ischemic_attack","HDL-C","LDL-C","cholesterol"]

replce_columns = {
    #u"客户样本编码":"sample_id",
    #u"性别":"gender",
    u"年龄":"age",
    u"身高(cm)":"height",
    u"体重(kg)":"weight",
    u"收缩压":"SBP",
    u"治疗后收缩压":"SBP_treated",
    u"舒张压":"DBP",
    u"是否吸烟(yes/no)":"current_smoker",
    u"双亲是否高血压(0/1/2)":"parental_hypertension",
    u"有无糖尿病(yes/no)":"diabetes",
    u"心血管病史(yes/no)":"prior_CVD",
    u"房颤(yes/no)":"AF",
    u"左心室肥大(yes/no)":"LVH",
    u"有过脑中风或者脑缺血发作(yes/no)":"prior_stroke_or_ischemic_attack",
    u"HDL-C-高密度蛋白(默认正常1.2，异常1)":"HDL-C",
    u"低密度蛋白(默认正常3.2，异常4.2)":"LDL-C",
    u"胆固醇(默认正常5，异常6.2)":"cholesterol"}


f = 'sample/20190724_115259_461.xls'
save_snp_info_csv(path='sample',f=f,snp_begin_column=0,info_begin_column=0,rename=True,replce_columns=replce_columns)
#@hyperHealthView.route('/PharChild_help',methods=['GET','POST'])
def PharChild_help():
    return render_template('PharChild_help.html')



#@hyperHealthView.route("/download/")
def downloader():
    file_name = request.values.get('file_name')
    print('==========downloader==============')
    print(file_name)
    print(basepath)
    print('========================')
    return send_from_directory(basepath, file_name, as_attachment=True) 

#@hyperHealthView.route("/download_template_excel")
def download_template_excel():
    #给产品经理填写的空白Excel模板
    file_name = 'relate_file/template_excel.xls'
    print('==========downloader==============')
    print(file_name)
    print(basepath)
    print('========================')
    return send_from_directory(basepath, file_name, as_attachment=True) 


#@hyperHealthView.route('/hyperHealthView/hyperHealth',methods=['GET','POST'])
def hyperHealth():
    if request.method == 'GET':
        return render_template('main.html', contents=u'瑞脉康TM脑卒中及冠心病风险检测（高血压）(RH-02)',title='hyperHealth',next_view='/hyperHealthView/hyperHealth')
    else:
        # 获取Excel文件:
        f = request.files['file']
        if not f:
            return 'please upload a excel file !'
        now  = datetime.datetime.now().strftime("%Y%m%d_%H%M%S") +'_'+ str(random.randint(0,1000))
        today = datetime.datetime.now().strftime("%Y%m%d")
        # 保存上传的文件
        print('============== 准备保存文件 ============== ')
        #filename,project_dir = save_upload_file(f,basepath,now,today,info_begin_column=0,replce_columns=replce_columns)
        filename,project_dir = save_upload_file(f,basepath,now,today,info_begin_column=0,rename=True,replce_columns=replce_columns)
        #save_snp_info_csv(path='sample',f=f,snp_begin_column=0,info_begin_column=0,rename=True,replce_columns=replce_columns)
        log_sh = os.path.join(project_dir,'log.sh')
        if os.path.isfile(log_sh):
            # 执行log.sh脚本：
            file_name_download = run_shell(project_dir,now,today,old_report_result_dir_name='result')
        return  render_template('download_page.html',file_name=file_name_download,view='hyperHealthView.downloader')


