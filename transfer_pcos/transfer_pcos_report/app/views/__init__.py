from flask import Blueprint

#pcosView = Blueprint('pcosView', __name__)
api = Blueprint('api', __name__)

# 写在最后是为了防止循环导入，ping.py文件也会导入 bp
#from app.views import  pcos,tokens
from app.views import  guoKeDa
