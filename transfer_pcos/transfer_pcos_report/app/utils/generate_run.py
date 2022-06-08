#encoding:utf8
import json,os
import requests 
import pandas as pd
import pysnooper
from app.utils.product import Products

from app.configs.config import basedir,Config
import argparse
import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except Exception as e:
    print(e)
class Generate_shell():
    #script_base = '/ifs1/Reotech/pub/biosoft/software/health_pipeline/AnlzRpt/' 
    script_base =  os.path.join(basedir,'app/AnlzRpt')
    def __init__(self,infile,out='.',is_impute='',chip_type='lasuo',is_update_product=''):
        self.out = out
        self.infile = infile 
        self.infile_txt = '.'.join(self.infile.split('.')[:-1])   +'.txt'
        self.is_impute = is_impute 
        self.chip_type = chip_type 
        self.is_update_product = is_update_product 
        self.all_sample = []
        self.all_sample_path = []
        self.msg = ''

    # 将对象及属性转为字典,当对实例化对象使用dict(obj)的时候, 会调用这个方法,这里定义了字典的键, 其对应的值将以obj['name']的形式取
    def keys(self):
        return {'all_sample','out','infile','infile_txt','all_sample_path'}

    #内置方法, 当使用obj['name']的形式的时候, 将调用这个方法, 这里返回的结果就是值
    def __getitem__(self,item):
        return getattr(self,item)

    #product_name 是从Excel里直接获取的中文名
    def gernerate_shell(self,sample,product_name,d):
        sample_path = d['sample_path']
        RunPipeline = os.path.join(self.script_base,'Scripts/RunPipeline.py')
        product = Products.config.get(product_name)
        if not product:
            # 在python2下的中文需要编码成utf-8，否则获取失败
            product = Products.config.get(product_name.encode('utf-8'))
        products_json = os.path.join(self.script_base,'Config/Product/{product}'.format(product=product))
        TplConfig = os.path.join(self.script_base,'Config/TplConfig/ASATplConfig.json')
        run1 ='python {RunPipeline} -i {self.out}/genotype.txt \\\n -w . -p {products_json}  \\\n-t ASA_CHIP \\\n -c {sample_path}/sample.json \\\n  -m {TplConfig}'.format(**locals())
        run2 = run1+ ' -g ' + ' {sample}/ImputationResult.txt'.format(sample=sample)
        return run1,run2

    # 每一份genotype.txt文件里有多个样品，没必要在做每个样品的时候再一次转格式,i就是记录到哪个样品了：
    def change_sola_2_guoke(self,i):
        shell_base = os.path.join(basedir ,'app/utils/change_sola_format.py')
        change_sola_2_guoke_shell = ''
        if i == 0:              # 如果是第一个样品，需要转换格式
            if self.chip_type == 'guoke': # 如果输入格式为果壳的数据芯片，则只需要重命名即可
                change_sola_2_guoke_shell =  f'mv   {self.infile_txt} {self.out}/genotype.txt && \\\n'
            elif self.chip_type == 'lasuo':                        # 如果输入为拉索的芯片，则需要转为果壳的芯片格式
                change_sola_2_guoke_shell = f'python {shell_base} {self.infile_txt} {self.out}/genotype.txt && \\\n'
        return change_sola_2_guoke_shell 
        
    def get_rs_from_genotype(self,d):
        #shell_base = os.path.join(basedir ,'app/utils/get_rs.py')
        TestItem = d.get('TestItem').strip()
        sample_path = d['sample_path']
        shell_base = os.path.join(basedir ,'app/utils/')
        python_shell = os.path.join(shell_base,'get_rs_db.py')        
        config_dir = os.path.join(shell_base,'project_type_need_rs.txt')
        get_rs_shell = 'python ' + python_shell  + f''' \\
        -i {self.out}/genotype.txt   \\
        -t guoke  \\
        -o {sample_path}/get_genotype_rs.txt  \\
        -m {sample_path}/missing_rs_ls.txt  \\
        -s {sample_path}/sample.json   \\
        -p \"{TestItem}\"  && \\\n'''
        return get_rs_shell 

    def generate_imput(self,d,i):
        '''
        生成的脚本结果:
        python /ifs1/Reotech/pub/biosoft/software/GenotypeImputation/Impute/GenotypeImputation.py -i genotype.txt -w . -c  /ifs1/Reotech/pub/biosoft/software/GenotypeImputation/Impute/Config/ImputationConfig.json -pos hg19_chr_pos_input.txt -s sample_list.txt

        python /ifs1/Reotech/user/huangzengfei/pyfile/imputation/GenotypeImputation_src/GenotypeImputation/Impute/GenotypeImputation.py -i random_genotype.txt  -w . -c /ifs1/Reotech/user/huangzengfei/pyfile/imputation/GenotypeImputation_src/GenotypeImputation/Impute/Config/ImputationConfig.json -l rs_random.txt  -s sample_list.txt
        '''
        #shell_base = '/ifs1/Reotech/pub/biosoft/software/GenotypeImputation/'
        SampleCode = d['SampleCode']
        sample_path = d['sample_path']
        Sample_product_dir = os.path.split(sample_path)[-1]
        Sample_product_dir = ''.join(Sample_product_dir.split()) # 去除文字中的空格
        Sample_product_dir = f'{SampleCode}_{Sample_product_dir}'
        shell_base = os.path.join(basedir ,'GenotypeImputation')
        GenotypeImputation = os.path.join(shell_base,'Impute/GenotypeImputation.py')
        util_shell_base = os.path.join(basedir ,'app/utils/')
        check_impute_result = os.path.join(util_shell_base,'check_impute_result.py')        
        ImputationConfig = os.path.join(shell_base,'Impute/Config/ImputationConfig.json')
        impute = '#! /bin/bash\n'
        impute =  impute +'source  /ifs1/Reohealth/project/report_on_web/venv_py37/bin/activate \n'
        impute =  impute + self.change_sola_2_guoke(i)
        impute =  impute + self.get_rs_from_genotype(d)
#        impute =  impute + f'\ntouch  {sample_path}/{SampleCode}_rs_result.txt'

        if self.is_impute:  # 如果需要做imputation，则添加下面的脚本
            impute =  impute +\
f'''python {GenotypeImputation}  \\
        -i  "{self.out}/genotype.txt"  \\
        -w  "{sample_path}" \\
        -c  "{ImputationConfig}" \\
        -l  "{sample_path}/missing_rs_ls.txt"   \\
        -s  "{sample_path}/sample_list.txt"   \\
        -g 6   \\
        -t 2  && \\
/bin/cp "{sample_path}/{SampleCode}/ImputationResult.txt" "{sample_path}" && \\
/bin/cat   "{sample_path}/get_genotype_rs.txt" "{sample_path}/{SampleCode}/ImputationResult.txt" > "{sample_path}/{Sample_product_dir}_rs_result.txt" && \\\n'''
        else:
            impute =  impute +\
f'''/bin/cp   "{sample_path}/get_genotype_rs.txt"  "{sample_path}/{Sample_product_dir}_rs_result.txt" && \\\n'''
# 添加那些仍未能impute出来的位点：
        TestItem = d.get('TestItem').strip()
        impute =  impute +\
f'''python {check_impute_result}  \\
        -i  "{sample_path}/{Sample_product_dir}_rs_result.txt"  \\
        -p  \"{TestItem}\" \n'''
#        impute =  impute +\
#'''/bin/rm -rf  {sample_path}/{SampleCode} \n'''   # 清理impute的缓存数据
        return impute


    #@pysnooper.snoop()
    def read_xls(self,sheet_name='OrderInfo'):
        from app.models.product import Product_rs,db 
        df = pd.read_excel(self.infile,sheet_name=sheet_name,encoding='utf-8')
        df['SampleDate'] = df['SampleDate'].apply(self.time_2_str)
        #print('=====================self.time_2_str============')
        #print(df['SampleDate'])
        #print('=====================self.time_2_str============')
        df['ReceiveDate'] = df['ReceiveDate'].apply(self.time_2_str)
        #print('=====================self.time_2_str============')
        #print(df['ReceiveDate'])
        #print('=====================self.time_2_str============')
        df['Birthday'] = df['Birthday'].apply(self.time_2_str)
        df['ReportDate'] = df['ReportDate'].apply(self.time_2_str)
        df['DeadLine'] = df['DeadLine'].apply(self.time_2_str)
        #print(df)
        #df['SpecificRequirements'] = df['SpecificRequirements'].apply(lambda x:x.encode('utf-8'))
        #df['Name'] = df['Name'].apply(lambda x:x.encode('utf-8'))
        df.fillna('',inplace=True)
        df_js_dict = df.to_dict(orient='records') 
        print(df.columns) 
        i = 0
        sample_lst = []
        for d in df_js_dict:
            sample =  str(d['SampleCode']) 
            #print('======----sample =====' )
            product_name = d['TestItem'].strip()
            sample_path = os.path.join(self.out,sample,product_name)
            self.all_sample.append(sample)
            self.all_sample_path.append(sample_path)
            d['sample_path'] = sample_path
            if not os.path.exists(sample_path):
                os.makedirs( sample_path  )

            if self.is_update_product:
                product = Product_rs.query.filter_by(product_name=product_name).first()
                if not  product:
                    product = Product_rs(product_name)
                    db.session.add(product)
                print(product_name)
                ret = requests.get(Config.REMOTE_DB__PRODUCT_RS_URL+'/query/get_product_rs?product_name='+product_name) 
                print('----------ret======')
                print(Config.REMOTE_DB__PRODUCT_RS_URL+'/query/get_product_rs?product_name='+product_name)
                try:
                    rs_lst = ','.join(json.loads(ret.text)['rs_list'] )
                except Exception as e:
                    rs_lst = None
                if rs_lst:
                    product.rs_lst = rs_lst
                    #print(rs_lst)
                    #print(product.rs_lst)
                else:
                    print('远程信息获取失败')
                    self.msg = '远程信息获取失败,'

            db.session.commit()

            # 生成sample.json文件
            with open(os.path.join(sample_path,'sample.json'),'w') as fh1:
                fh1.write(json.dumps(d,ensure_ascii=False))
            # 生成sample.txt文件
            with open(os.path.join(sample_path,'sample_list.txt'),'w') as fh2:
                fh2.write(sample+'\n')
            # 生成run1.sh run2.sh
            with open(os.path.join(sample_path,'run1.sh'), 'w') as fh1,\
                 open(os.path.join(sample_path,'run2.sh'), 'w') as fh2:
                run1,run2 = self.gernerate_shell(sample_path,product_name,d)
                fh1.write(run1)
                fh2.write(run2)
            # 生成 impute.sh
            # 这里加sample in sample_lst 判断的原因是，某时候产品经理可能有重复的样品+重复的产品
            #if  not sample in sample_lst:
            imput_full_path =os.path.join(sample_path,'impute.sh') 
            if  not os.path.exists(imput_full_path) :
                with open(imput_full_path,'w') as fh3:
                    impute = self.generate_imput(d,i)
                    fh3.write(impute)
            i += 1
            sample_lst.append(sample)
            

    # 将Excel里面的时间类型转为字符串
    def time_2_str(self,x):
        if pd.isnull(x):
            return str(x)
            #return x
        try:
            return x.strftime('%Y.%m.%d')
        except AttributeError:
            print('error ---------x.strftime AttributeError ----'*2)
            return str(x)
        except Exception :
            raise

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i' ,'--in_excel',help='请输入Excel文件，以生成run1.sh run2.sh 和配置文件')
    parser.add_argument('-o' ,'--out',help='输入的目录地址，默认本地目录')
    args = parser.parse_args()
    infile =  args.in_excel
    outdir = args.out or '.'
    if not infile:
        os.sys.exit('由于未输入 Excel文件作为参数，程序已经中断\n请用重新运行，用-e 参数来添加Excel文件。')
    s =Generate_shell(infile,outdir) 
    tb = s.read_xls()

if __name__ == '__main__':
    main()


