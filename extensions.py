#!/usr/bin/env python3
# -*- coding: utf-8 -*-
''' Create instance of these flask extensions '''
import logging,os
from logging.handlers import TimedRotatingFileHandler


if not  os.path.exists('./logs'):
    os.makedirs('./logs')
# 默认的配置
DEFAULT_LOG_LEVEL = logging.INFO    # 默认等级
DEFAULT_LOG_FMT = '%(asctime)s %(filename)s [%(lineno)d] %(levelname)s: %(message)s'   # 默认日志格式
DEFUALT_LOG_DATEFMT = '%Y-%m-%d %H:%M:%S'  # 默认时间格式
DEFAULT_LOG_FILENAME = './logs/flask_run.log'    # 默认日志文件名称

class Logger():
    def __init__(self):
        self.__logger = logging.getLogger()
        self.formatter = logging.Formatter(fmt=DEFAULT_LOG_FMT,datefmt=DEFUALT_LOG_DATEFMT)
        #self.__logger.addHandler(self._get_file_handler(DEFAULT_LOG_FILENAME))
        self.__logger.addHandler(self._get_time_handler(DEFAULT_LOG_FILENAME))
        self.__logger.setLevel(DEFAULT_LOG_LEVEL)


    def _get_time_handler(self,filename):
        # timehandler = TimedRotatingFileHandler(filename,when='S',interval=1,backupCount=3,encoding='utf-8')
        timehandler = TimedRotatingFileHandler(filename=filename, when='D', backupCount=10, encoding='utf-8')
        #rotateHandler = ConcurrentRotatingFileHandler(filename, "a", 512*1024, 5)
        #rotateHandler = ConcurrentRotatingFileHandler(filename, "a", 512, 5)
        #self.__logger.addHandler(rotateHandler)
        #timehandler.suffix = '%Y-%m-%d.%H:%M:%S.log'
        timehandler.suffix ="%Y-%m-%d_%H-%M-%S.log"
        self.formatter = logging.Formatter(fmt=DEFAULT_LOG_FMT,datefmt=DEFUALT_LOG_DATEFMT)
        timehandler.setFormatter(self.formatter)
        return timehandler

    @property
    def logger(self):
        return self.__logger

logger = Logger().logger
