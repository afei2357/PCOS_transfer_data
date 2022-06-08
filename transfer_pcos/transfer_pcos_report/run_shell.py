from flask_script  import Manager
from app  import create_app,db
#from app.models1  import WeChat,OrderHlth,OrderGnic,OrderMed
from app.models.product   import  Reports
app  = create_app()
manager = Manager(app)

#manager.add_command("showurls",ShowUrls())
@manager.shell
def make_shell_context():
    #return dict(app=app,db=db,User=User,WeChat=WeChat,OrderHlth=OrderHlth,OrderGnic=OrderGnic,OrderMed=OrderMed)
    return dict(Reports=Reports)
# 使用方法：
# python  run_shell.py shell
if __name__ == '__main__':
    manager.run()

