import sqlite3
from flask import Flask
#from  flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from app.configs.config import Config
from flask_cors import CORS

#from celery import Celery
#celery = Celery(__name__,backend=Config.CELERY_BACKEND,broker=Config.CELERY_BROKER)
#from celery.utils.log import get_task_logger
#celery_logger = get_task_logger('run_celery_logger')
#cors = CORS(supports_credentials=True)
cors = CORS()
db = SQLAlchemy()

def create_app(config=Config):
    app = Flask(__name__)
    from app.views import pcosView
    app.config.from_object(Config)
    db.init_app(app)
    #cors.init_app(app,supports_credentials=True)
    CORS(app,resources=r'/*',supports_credentials=True)
    #bootstrap = Bootstrap(app)
    #celery.conf.update(app.config)

    app.register_blueprint(pcosView)

    return app

#conn = sqlite3.connect('report_database.db')
#c = conn.cursor()
#c.execute(''' CREATE TABLE COMPANY
#         (ID INT PRIMARY KEY     NOT NULL, SALARY         REAL);'''
#        )
#conn.commit()
#conn.close()

