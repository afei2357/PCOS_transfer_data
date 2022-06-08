#encoding:utf-8
import sys,os
import argparse,pysnooper
import configparser
import json 
now_path  =  os.path.abspath( os.path.dirname(__file__))
sys_root = os.path.abspath(now_path + '/../..') 
print('---------------sys_root==============')
print(sys_root)
print('---------------sys_root==============')
#sys.path.append('/ifs1/Reohealth/project/report_on_web/v2.0')
sys.path.append(sys_root)
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except Exception as e:
    print(e)
# 判断是拉索的还是果壳的数据格式
def which_format(infile,format_name):
    with open(infile) as fh:
        line1 = fh.readline() 
        if format_name == 'lasuo' and  line1.startswith('gxid'):
            return 'lasuo'
        elif format_name == 'guoke' :
            for line in fh:
                if line.startswith('##'):
                    continue
                elif line.startswith('#CHROM'):
                    return 'guoke' 
    return False

# 从数据库中获取不同项目所需要的rs位点，比如包括 RK-08儿童多元智能,RC-04_瑞安佳,Rk-10精准用药,PK-03常见疾病等项目
def get_need_rs(project):
    from app import  create_app
    app = create_app()
    with app.app_context():
        from app.models.product import Product_rs
        print('product---------')
        product = Product_rs.query.filter_by(product_name=project).first()
        print(product)
        if product:
            rs_lst = product.rs_lst
            rs_lst = set([ rs.strip() for rs in rs_lst.split(',') ] ) 
            print('product.rs_lst,rs_lst---------')
            print(rs_lst)
            return rs_lst
        
# 拉索的首行：
# gxid    chromosome      position        R190652
# 果壳的前几行：
# ##FileFormat=ASA-CHIA1.0
# ...
# #CHROM  POS     ID      REF     INFO    R190064 R190967
# 从输入的芯片文件中获取欲提取的rs的具体基因型
def get_want_rs(infile,sample_name,format_name) :
    rs_dict = {}
    with open(infile) as fh:
        for line in fh:
            line = line.strip()
            if line.startswith('##'):
                continue
            if line.startswith('#') or line.startswith('gxid'): # gxid是拉索的列标题
                lst  = line.split()
                print('------------lst==================')
                print(lst)
                print(lst[-1] == sample_name)
                print(len(lst[-1]))
                print(len(sample_name))
                print('------------lst==================')
                sample_index = lst.index(sample_name) 
            if line:
                items = line.split()
                if format_name == 'guoke':
                    rs,chr,pos,val = items[2],items[0],items[1],items[sample_index] 
                elif format_name == 'lasuo':
                    rs,chr,pos,val = items[0],items[1],items[2],items[sample_index] 
                if rs.endswith('a'):
                    rs = rs.rstrip('a')
                rs_dict[rs] = val
    return rs_dict

# 将 genotype.txt里找到或者未找到的rs信息写出到文件
def write_rs(snp_outfile,rs_dict,want_rs,miss_out_file,sample_name='-'):
    with open(snp_outfile,'w') as fh,open(miss_out_file,'w') as ms:
        fh.write('ID\t'+sample_name+'\n')
        for rs in want_rs:
            if (rs_dict.get(rs,'-') != '-') and  ( rs_dict.get(rs) != '--') :
                fh.write(rs+'\t')
        #fh.write('\n')
        #for rs in want_rs:
                fh.write(rs_dict.get(rs,'-')+'\n')
        for rs in want_rs:
            if not (rs in rs_dict) or  rs_dict.get(rs) == '--' or  rs_dict.get(rs) == '-':
                ms.write(rs+'\n')

#@pysnooper.snoop()
def main():
    parser = argparse.ArgumentParser()
    dir =  os.path.abspath(os.path.dirname(__file__))
    project_file = os.path.join(dir,'project_type_need_rs.txt')

    parser.add_argument('-i','--input',help="输入的基因型文件")	
    parser.add_argument('-t','--intype',help="输入的基因型文件文件的类型，拉索或者果壳两个公司给的文件格式不一样。",choices=["lasuo","guoke"])	
    parser.add_argument('-o','--output',help="输出的结果文件")	
    parser.add_argument('-m','--missing',help="输出的缺失的rs的文件名",default='missing.txt')	
    parser.add_argument('-p','--project',help="需要哪些项目的rs,对应配置文件里的第一列可以看到这个")	

    parser.add_argument('-s','--sample',type=str,help='在基因型文件中的对应的样本编码或者是json格式的样本信息,例如类型如下信息:\n{"InfoCode": 200001, "ClientCode": "V2003485", "Name": "唐国斌", "SampleCode": "R190851", "Gender": "男", "Birthday": "76", "Tel": 13510014835, "Height": "", "Weight": "", "Waistline": "", "Nation": "汉", "SampleDate": "2020.01.02", "ReceiveDate": "2020.01.02", "ReportDate": "2020.01.07", "TestItem": "RHM002 个人基因组基础版", "SampleType": "口腔拭子", "Template": 0, "DeadLine": "2020.01.22", "Agent": "卓壮医疗", "SpecificRequirements": "瑞奥模板", "OfflineReport": ""}')	

    args = parser.parse_args()
    print('------------args.project_db') 
    print(args.project) 
#    print(project)
    print('------want_rs===')
    if os.path.exists(args.sample) and os.path.isfile(args.sample):
        with open(args.sample) as fh:
            sample_json = json.load(fh)
            TestItem = sample_json.get('TestItem')
            #print(TestItem)
            sample = sample_json.get('SampleCode')
    else:
        sample = args.sample


    #print(args.project)
    sample = str(sample)
    rs_dict = get_want_rs(args.input,sample,args.intype) 
    #print(rs_dict)

    #config = 'project_type_need_rs.txt'
    #item = get_need_rs(args.config)
    #print('------item===')
    #print(item)
    #want_rs = item['RE0D05_heart_blood_drug'] 
    print(args.project)
    #want_rs = item[want_product_english] 
    want_rs = get_need_rs(args.project) 
    #print('------want_rs===')
    print(want_rs)
    #want_rs = project
    #miss_out_file ='miss_out_file'
    write_rs(args.output,rs_dict,want_rs,args.missing,sample)

if __name__ == '__main__':
    main()
