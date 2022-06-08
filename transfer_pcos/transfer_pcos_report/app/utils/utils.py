#encoding:utf-8
#import pandas as pd
import os
#import tarfile
import shutil
import subprocess as sp 
#import pysnooper
 

# 下列函数，如果某个目录不存在，就创建这个目录
def if_not_exist_file_mkdir(fullpath):
    if not os.path.exists(fullpath):
         os.makedirs(fullpath)

# 下列函数用于压缩某个文件夹
def compress(tar_name,path):
    with tarfile.open(tar_name,"w:gz") as tar:  
        for root,dir,files in os.walk(path):
            root_ = os.path.relpath(root,start=path+'/..')
            for file in files:
                full_path = os.path.join(root,file)
                tar.add(full_path,arcname=os.path.join(root_,file))

 

# 下列函数用于保存上传的文件        
def save_upload_file(f,basepath,now,today,file_type='csv',snp_begin_column=0,info_begin_column=1,rename=True,replce_columns=False):
    file_type_sup = os.path.splitext(f.filename)[-1] # 获取文件后缀
    filename = now + file_type_sup
    upload_path = os.path.join(basepath,'upload_files')
    if_not_exist_file_mkdir(upload_path)
    upload_path_full = os.path.join(upload_path,filename)
    print('------------ in save_upload_file ,saving file: ')
    print(upload_path_full)
    f.save(upload_path_full)
    # 一天一个文件夹，如：report_on_web/work_dir/PharChild/20190612 
    today_dir = os.path.join(basepath,today)
    if_not_exist_file_mkdir(today_dir)    
    # 某个项目在日期的文件夹内，由于每天可能有不同的项目，因此在日期文件夹内，还按时间来安排项目，如：
    # 如： report_on_web/work_dir/PharChild/20190612/20190612_171325_16 最后的数字16 是一个随机数
    project_dir = os.path.join(today_dir,now)
    # 如果basepath = '/ifs1/Reohealth/project/report_on_web/v2.0/work_dir/PharChild'
    base_split = basepath.split('/')
    #现在 base_split = ['', 'ifs1', 'Reohealth', 'project', 'report_on_web', 'v2.0', 'work_dir', 'PharChild']   
    base_parent = '/'.join(base_split[:-2])
    # base_parent = '/ifs1/Reohealth/project/report_on_web/v2.0'
    project = base_split[-1]
    # template_path = '/ifs1/Reohealth/project/report_on_web/v2.0/template_files/PharChild'
    template_path = os.path.join(base_parent,'template_files/'+project)
    template = os.path.join(template_path,'template')
    shutil.copytree(template,project_dir)
    if file_type == 'csv':
        print('====================  in if file_type == csv: ')
        save_snp_info_csv(path=project_dir,f=f,snp_begin_column=snp_begin_column,info_begin_column=info_begin_column,rename=rename,replce_columns=replce_columns)
    else:
        pass
    return filename,project_dir

# 下列函数用于执行以 'log.sh' 的shell脚本
def run_shell(project_dir,now,today,old_report_result_dir_name='phar_result'):
    cwd = os.getcwd()
    print('before run,the cwd is :\n'+os.getcwd())
    os.chdir(project_dir)
    print('after run,the cwd is :\n'+os.getcwd())
    sp.call('./log.sh')
    #return 'tesssss'
    os.chdir(cwd)
    print('after run and chdir ,the cwd is :\n'+os.getcwd())
    uncompress_result_files = os.path.join(project_dir,old_report_result_dir_name)
    print('uncompress_result_files')
    print(uncompress_result_files)
    compress_result_files = project_dir+'/'+now+'_result.tar.gz'
    file_name = now+'_result.tar.gz'
    compress(compress_result_files,uncompress_result_files)
    # file_name_download 变量是用于下载的，
    #其形式为：20190612/2019.06.12_16.36.07/2019.06.12_16.36.07_result.tar.gz 
    file_name_download = today+'/'+ now +'/' +file_name
    return file_name_download



# 将Excel 保存为csv格式的文件
# Excel里面有两个sheet，分别名为snp和info，snp里的表是各个位点的测序情况，
 #info是样本的信息情况，其中info的第一列是"信息卡编号"，因此跳过info的第一列
def save_snp_info_csv(path,f,snp_begin_column=0,info_begin_column=1,rename=True,replce_columns=False):
    print('======= save_snp_info_csv ing ===============')
    snp = read_xls(f,sheet_name='snp',begin_column=snp_begin_column)
    snp = rename_df(snp)
    snp.to_csv(os.path.join(path,'sample_snp.tsv'),sep='\t',index=False,header=True,encoding='utf8')
    try:
        info = read_xls(f,sheet_name='info',begin_column=info_begin_column)
        print(' ===================the info is1 ===================:')
        # 是否替换掉原来Excel表的列标题。replce_columns 是一个list
        if replce_columns:
            info.rename(columns=replce_columns,inplace=True)
    
        if rename:
            info = rename_df(info)
            print(info.columns)
            try:
                gender = info[['#sample_id','gender']]
                gender.to_csv(os.path.join(path,'sample_gender.tsv'),sep='\t',index=False,header=True,encoding='utf8')
            except Exception as e:
                print(e)
                print('gender can not to be save ')
        info.to_csv(os.path.join(path,'sample_info.tsv'),sep='\t',index=False,header=True,encoding='utf8')
    except Exception as e:
        print(e)
        print('info  is not exst in Excel ')
        


if __name__ == '__main__':
    #path = '/ifs1/Reohealth/project/report_on_web/work_dir/Jiujing/20190613/20190613_142942_950/result_alcohol'
    #compress('test.tar.gz',path)
    #save_snp_info_csv('.','PharChild.xlsx')

    #read_xls(filename='20190704_120456_879.xlsx',sheet_name='snp',begin_column=1)
    save_snp_info_csv(filename='20190724_115259_461.xls',sheet_name='info',begin_column=0)
