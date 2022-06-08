import sys,os
import argparse,pysnooper
import configparser
import json 
now_path  =  os.path.abspath( os.path.dirname(__file__))
sys_root = os.path.abspath(now_path + '/../..') 
#sys.path.append('/ifs1/Reohealth/project/report_on_web/v2.0')
sys.path.append(sys_root)

#获取那份提取的rs文件与Imputation_result.txt 合并后的结果文件，
def get_merge_result(merge_file):
    merge_rs_dict = {}
    with open(merge_file,'r') as fh:
        for line in fh:
            line = line.strip()
            if line.startswith('#') or line.startswith('ID'):
                continue
            rs,var = line.split()
            merge_rs_dict[rs] = var
    return merge_rs_dict


#获取数据库里的rs和其ref,用于补充那些impute不出来的位点
def get_rs_dict_from_db():
    from app import  create_app
    rs_dict = {}
    app = create_app()
    with app.app_context():
        from app.models.product import Rs
        all_rs = Rs.query.all()
        for rs in all_rs:
            #rs_dict['rs'] = rs.rs_name
            rs_dict[rs.rs_name] = rs.ref
        return rs_dict

# 将缺失的rs写入结果文件            
def write_in_merge_result(remain_miss_rs,rs_dict,merge_file,remain_miss_rs_file_name):
    #with open(merge_file,'a') as fh,open(remain_miss_rs_file_name,'w') as out2 :
    #    for rs in remain_miss_rs:
    #        if rs_dict.get(rs):
    #            fh.write(rs+'\t'+rs_dict[rs]+'\n')
    #        else:
    #            out2.write(rs+'\n')
    with open(remain_miss_rs_file_name,'w') as out2 :
        for rs in remain_miss_rs:
            out2.write(rs+'\n')

def main():
    from app.utils.get_rs_db import get_need_rs
    print('---------------')
    parser = argparse.ArgumentParser()
    dir =  os.path.abspath(os.path.dirname(__file__))
    #project_file = os.path.join(dir,'project_type_need_rs.txt')

    #parser.add_argument('-m','--missing',help="缺失的rs的文件名",default='missing.txt')
    parser.add_argument('-i','--inpute',help="提取的rs文件与Imputation_result.txt 合并后的结果文件")
    parser.add_argument('-p','--project',help="需要哪些项目、产品的rs,对应配置文件里的第一列可以看到这个")
    args = parser.parse_args()
    want_rs = get_need_rs(args.project) 
    add_rs_dict = get_rs_dict_from_db()
    merge_result = get_merge_result(args.inpute)

    remain_miss_rs = set([i.strip() for i in want_rs]) - set([i.strip() for i in merge_result.keys()]) 
    #remain_miss_rs = set( want_rs) - set( merge_result.keys()) 
    print(remain_miss_rs)
    print(want_rs)
    print(merge_result.keys())
    print(add_rs_dict.keys())
    remain_miss_rs_file_name = args.inpute.strip('rs_result.txt') + '_remain_miss_rs.txt'
    if remain_miss_rs:
        write_in_merge_result(remain_miss_rs,add_rs_dict,args.inpute,remain_miss_rs_file_name)


if __name__ == '__main__':
    main()
