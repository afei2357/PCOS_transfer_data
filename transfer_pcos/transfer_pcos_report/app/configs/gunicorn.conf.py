# 监听IP和端口，也可以写'0.0.0.0:port',则在所有网卡上监听
#bind = '127.0.0.1:5000'
bind = '0.0.0.0:7000'
#bind = '0.0.0.0:9000'
# 服务无响应（不返回）被重启的时间阈值
timeout = 30
#worker_class = 'gevent'
worker_class = 'sync'

# This refers to the number of clients that can be waiting to be served.
#backlog = 512

# 工作目录
chdir = './'

# 并行工作进程数，默认 1
workers=1
# 指定每个进程的线程数， 默认 1
threads=1

# 检测到代码改动是否重启服务
reload = True
## 将服务放入后台不受终端的影响
#daemon = False
#
## stdout/stderr 是否重定向到错误日志
#capture_output = False
#
## 日志相关
#loglevel = 'info' 
#access_log_format = '%(t)s %(p)s %(h)s "%(r)s" %(s)s %(L)s %(b)s %(f)s" "%(a)s"'
## 连接的IP等信息会记入accesslog日志
#accesslog = "./logs/gunicorn.log"
### 包括重启在内的一些信息会记录在错误日志
#errorlog = "./logs/gunicorn.err"
#LOGGING = {
logconfig_dict = {
    'version':1,
    'disable_existing_loggers': False,
    'loggers':{
        "gunicorn.error": {
            #"level": "DEBUG",# 打日志的等级可以换的，下面的同理
            "level": "INFO", # 打日志的等级可以换的，下面的同理
            "handlers": ["error_file"], # 对应下面的键
            "propagate": 1,
            #"qualname": "gunicorn.error"
        },

        "gunicorn.access": {
            #"level": "DEBUG",
            "level": "INFO", # 打日志的等级可以换的，下面的同理
            "handlers": ["access_file"],
            "propagate": 0,
            #"qualname": "gunicorn.access"
        }
    },
    'handlers':{
        "error_file": {
            "class": "logging.handlers.RotatingFileHandler",
            #"maxBytes": 1024*1024*1024,# 打日志的大小，我这种写法是1个G
            "maxBytes": 1024*1024*10, # 打日志的大小,取10M
            "backupCount": 10, # 备份多少份，经过测试，最少也要写1，不然控制不住大小
            "formatter": "generic", # 对应下面的键
            # 'mode': 'w+',
            "filename": "./logs/gunicorn.error.log" # 打日志的路径
        },
        "access_file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "when":"D",
            "backupCount": 10,
            "formatter": "generic",
            "filename": "./logs/gunicorn.access.log",
        },
        #"access_file": {
        #    "class": "logging.handlers.RotatingFileHandler",
        #    "maxBytes": 1024*1024*10, # 打日志的大小,取10M
        #    "backupCount": 10,
        #    "formatter": "generic",
        #    "filename": "./logs/gunicorn.access.log",
        #},
        "console": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "generic",
        }
    },
    'formatters':{
        "generic": {
            #"format": "'[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s'", # 打日志的格式
            "format": " %(message)s", # 打日志的格式
            "datefmt": "[%Y-%m-%d %H:%M:%S %z]", # 时间显示方法
            "class": "logging.Formatter"
        },
        "access": {
            #"format": "'[%(process)d] [%(asctime)s] %(levelname)s [%(filename)s:%(lineno)s] %(message)s'",
            "format": "' [%(asctime)s]  %(message)s'",
            "class": "logging.Formatter"
        }
    }
}
# 出现 Error: Unable to configure root logger:的错误，可以在上面的handlers里面添加一个console的key
# 或者用下面的方法：
#logconfig_dict['root'] = {
#    'level': 'WARNING',
#    'handlers': ['web_console'],
#}
