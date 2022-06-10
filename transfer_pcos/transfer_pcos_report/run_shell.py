from flask_script  import Manager
from app  import create_app,db
#from app.models1  import WeChat,OrderHlth,OrderGnic,OrderMed
from app.models.models_user   import  User
from app.models.models_pcos   import  Reports
app  = create_app()
manager = Manager(app)

#manager.add_command("showurls",ShowUrls())
@manager.shell
def make_shell_context():
    return dict(Reports=Reports,User=User)
# 使用方法：
# python  run_shell.py shell
if __name__ == '__main__':
    manager.run()

