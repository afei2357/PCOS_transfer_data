
#encoding:utf8
from utils import save_snp_info_csv,save_upload_file
from hyperHealth import replce_columns
replce_columns_22 = {
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

