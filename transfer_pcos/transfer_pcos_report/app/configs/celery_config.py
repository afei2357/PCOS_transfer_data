import logging.config
LOG_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    #'disable_existing_loggers': True,
    'loggers': {
         'run_celery_logger': {
            'handlers': ['celery_handler'],
            'level': 'INFO',
            'propagate': True,
         }
    },
    'handlers': {
        'celery_handler': {
             'level': 'INFO',
             'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'simple',
            #'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': './logs/celery.log',
            'backupCount': 5,
            'maxBytes': 1024*1025*10,
            #'when': 'midnight',
            'encoding': 'utf-8',
        },
    },
    'formatters': {
        'simple': {
            # 'datefmt': '%m-%d-%Y %H:%M:%S'
            'format': '%(asctime)s \"%(pathname)s：%(module)s:%(funcName)s:%(lineno)d\" [%(levelname)s]- %(message)s'
        }
    }
}
  
logging.config.dictConfig(LOG_CONFIG)

