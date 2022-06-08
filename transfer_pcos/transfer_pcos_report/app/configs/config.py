#encoding:utf8
import os 
config_dir = os.path.abspath(os.path.dirname(__file__))
basedir = os.path.abspath( os.path.join(config_dir,'../..') )


class Config():
    SECRET_KEY = 'HARD TO GUESS'
    BASEDIR = basedir
    REMOTE_DB__PRODUCT_RS_URL = 'http://47.107.181.212:7000' 
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    #SQLALCHEMY_DATABASE_URI = 'mysql://root:reo123@localhost:3306/new_omics?charset=utf8'
    #SQLALCHEMY_DATABASE_URI = 'mysql://hzf:123456@omics.cblink.net:3306/omics'
    SQLALCHEMY_DATABASE_URI = \
        'mysql://root:reo123@localhost:3306/transfer_pcos?charset=utf8mb4' or \
        'sqlite:///'+os.path.join(basedir,'transfer_pcos.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = True 
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
    FLASKY_MAIL_SUBJECT_PREFIX = 'test'    


    MAIL_SERVER = 'smtp.qiye.aliyun.com' 
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    #MAIL_USE_SSL = False
    MAIL_USE_TSL = False 
    MAIL_USERNAME = 'huangzengfei@reohealth.cn'  
    MAIL_SENDER = 'huangzengfei@reohealth.cn'  
    #MAIL_PASSWORD = '这是我的邮箱密码'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') # 在~/.bashrc里写入 export MAIL_PASSWORD=我的邮箱密码
    #如果邮箱为163邮箱，密码为你在163邮箱里面的  （设置 -> POP3/SMTP/IMAP -> 客户端授权密码） 里面设置的,而不是实际你登录163邮箱的密码
    # celery配置：
    CELERY_BACKEND = 'redis://localhost:6379'
    CELERY_BROKER = 'redis://localhost:6379'

view_dict = {
    'pcosView.pcos':u'发送pcos报告至妇幼保健院信息科',
}
