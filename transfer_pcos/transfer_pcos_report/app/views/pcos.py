#encoding:utf8
import os,random,sys,re
from datetime import datetime
import shutil
#import pysnooper 

from flask import  Flask,jsonify,request,make_response,render_template,flash,redirect,url_for,abort,send_from_directory
from app.configs.config import basedir
from app.models.product import Reports 
from app.utils.utils import if_not_exist_file_mkdir
from app.utils.utils_pcos import *
import requests
from flask_cors import cross_origin

from . import pcosView 

basepath = os.path.join(basedir,'work_dir/pcos')

@pcosView.route('/pcosView/pcos/',methods=['GET','POST'])
#@pysnooper.snoop(prefix='-chip- \t')
def pcos():
    if request.method == 'GET':
        return render_template('pcos.html', contents=u'pcos妇幼',title="pcos",next_view='/pcosView/pcos/')
    else:
        # 获取Excel文件:
        files = request.files.to_dict()
        # excel 是上传的Excel文件
        zipfile = files.get('file')
        print('ziofile----')
        print(request.form)
        print('request.form')
        print(request.args)
        print(request.values)
        print(request.files)
        print(zipfile)
        if not (zipfile) :
            return 'please upload a zip file  !'
        now  = datetime.now().strftime("%Y%m%d_%H%M%S") +'_'+ str(random.randint(0,1000))
        today =datetime.now().strftime("%Y%m%d")
        # 保存上传的文件
        filename,project_dir = save_upload_file(zipfile,basepath,now,today)
        # 上传的Excel表格的全路径
        zip_full_path = os.path.join(project_dir,filename)
        xml_path = os.path.join(project_dir,'xml') 
        unzip_path = os.path.join(project_dir,'unzip') 
        if_not_exist_file_mkdir(xml_path)
        if_not_exist_file_mkdir(unzip_path)
        #out_result_path = unzip_file(zip_full_path,unzip_path)
        unzip_file(zip_full_path,unzip_path)
        files = list_all_files(unzip_path)
        result_info = []
        for xls in files:
            result_info.append( main_send_2type(xls)  )
            #pass
        
        print('zip_full_path--------')
        print(zip_full_path)
        print(project_dir)
        print(unzip_path)

        print(files)
        flash(  u" 项目后台地址：\n    " )
        flash(  str(project_dir) )
        flash(  u" 各个报告的发送结果如下：  " )
        
        for info in result_info:
            flash(  info  )
        return redirect(url_for('pcosView.pcos'))
        #return  u"</p> 项目正在运行，运行完毕后会自动发送邮件. </p> </p>接收报告的邮箱地址：</p>" + email+ "</p></p>项目后台地址：</p>    "+str(project_dir)

#@pcosView.route('/pcosView/info/',methods=['GET','POST'])
#@pysnooper.snoop(prefix='-chip- \t')
#@cross_origin(supports_credentials=True)
@pcosView.route('/pcosView/list/',methods=['GET','POST'])
def pcos_infos():
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    #paginate_query = Reports.query.order_by(Reports.id.desc())\
    paginate_query = Reports.query.order_by(Reports.update_time.desc())\
            .paginate(page, page_size)
    datas = paginate_query.items
    print('item data ')
    print( datas)
    data_info ={'items': [item.to_dict() for item in datas], 
                    '_meta': {
                        'page': page,
                        'page_size': page_size,
                        'total_pages': paginate_query.pages,
                        'total_items': paginate_query.total
                    }}
    return jsonify({'code': 200, 'infos': data_info})
    #return 'info '

#@pcosView.route('/pcosView/test/',methods=['GET','POST'])
@pcosView.route('/pcosView/info/',methods=['GET','POST'])
#@pysnooper.snoop(prefix='-chip- \t')
def test_celery_pcos():
    #from app.utils.run_imputation import test
    #test.delay()
    print('in vie')
    #logger.info('in vie')
    return 'indexView_index\n'

@pcosView.route('/pcos_help/',methods=['GET','POST'])
def pcos_help():
    return render_template('chip_help.html')


# 下列函数用于保存上传的文件        
#@pysnooper.snoop(prefix='-save_upload_file- \t')
def save_upload_file(f,basepath,now,today):
    file_type_sup = os.path.splitext(f.filename)[-1] # 获取文件后缀
    #filename = now + '_' + f.filename
    filename = now + file_type_sup
    # 一天一个文件夹，如：report_on_web/work_dir/chip/20190717
    today_dir = os.path.join(basepath,today)
    if_not_exist_file_mkdir(today_dir)    
    # 某个项目在日期的文件夹内，由于每天可能有不同的项目，因此在日期文件夹内，还按时间来安排项目，如：
    project_dir = os.path.join(today_dir,now)
    if_not_exist_file_mkdir(project_dir)    
    upload_path_full = os.path.join(project_dir,filename)
    f.save(upload_path_full)
    return filename,project_dir


