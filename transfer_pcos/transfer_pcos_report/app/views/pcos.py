#encoding:utf8
import os,random,sys,re
from datetime import datetime
import shutil
from app.views.auth import token_auth
from app import db
#import pysnooper 

from flask import  Flask,jsonify,request,make_response,render_template,flash,redirect,url_for,abort,send_from_directory
from app.configs.config import basedir
from app.models.models_pcos import Reports 
from app.utils.utils import if_not_exist_file_mkdir
from app.utils.utils_pcos import *
import requests
from flask_cors import cross_origin

from . import pcosView 

basepath = os.path.join(basedir,'work_dir/pcos')

@pcosView.route('/api/pcos',methods=['GET','POST'])
@token_auth.login_required
def pcos():
    if request.method == 'GET':
        return render_template('pcos.html', contents=u'pcos妇幼',title="pcos",next_view='/pcosView/pcos/')
    else:
        # 获取Excel文件:
        files = request.files.to_dict()
        # excel 是上传的Excel文件
        zipfile = files.get('file')
        print('ziofile----')
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
        result_info_tmp = []
        result_info = []
        for xls in files:
            result_info_tmp.append( main_send_2type(xls)  )
        
        for lst1,lst2 in result_info_tmp:
            result_info.append(lst1)
            result_info.append(lst2)
        print('zip_full_path1--------')
        print(result_info) 
        print('zip_full_path2--------')
        print(zip_full_path)
        print(project_dir)
        print(unzip_path)

        print(files)
        return jsonify({'code': 200, 'infos': result_info})
    #return redirect(url_for('pcosView.pcos'))

#@pcosView.route('/pcosView/list_all',methods=['GET','POST','OPTIONS'])
@pcosView.route('/api/list',methods=['GET','POST'])
@token_auth.login_required
def pcos_infos():
    print('aaaa')
    filter_list = []
    ### 获取 get过来的信息
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)
    name = request.args.get('name',type=str, default=None)
    lis_Barcode = request.args.get('lis_Barcode',type=str, default=None)
    clazz = request.args.get('clazz',type=str, default=None)
    info = request.args.get('info',type=str, default=None)

    ### 搜索关键词
    if lis_Barcode:
        filter_list.append(Reports.lis_Barcode.like('%'+lis_Barcode+'%'))
    if name:
        filter_list.append(Reports.name.like('%'+name+'%'))
    if clazz:
        filter_list.append(Reports.clazz.like('%'+clazz+'%'))
    if info:
        filter_list.append(Reports.info.like('%'+info+'%'))

    #paginate_query = Reports.query.order_by(Reports.id.desc())\
    paginate_query = Reports.query.filter(*filter_list)\
                     .filter(Reports.delete_at== None)\
                     .order_by(Reports.id.desc())\
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
    #headers = {
    #    'Content-Type': 'application/json',
    #    'Access-Control-Allow-Origin': '*',
    #    'Access-Control-Allow-Methods': '*',
    #    'Access-Control-Allow-Headers': '*',
    #}
    return jsonify({'code': 200, 'infos': data_info})

@pcosView.route('/pcosView/info',methods=['GET','POST'])
@pcosView.route('/pcosView/list2',methods=['GET','POST'])
@token_auth.login_required
def test_celery_pcos():
    print('in vie')
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


# 删除一个订单
@pcosView.route('/api/pcosView/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_order_pcos( id):
    report = Reports.query.get_or_404(id)
    report.delete_at = datetime.now()
    db.session.commit()
    return jsonify({'code': 200, 'msg': "删除成功"})

