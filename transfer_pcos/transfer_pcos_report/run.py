#encoding:utf8 
import os,json
from flask_sqlalchemy import SQLAlchemy
#from app import create_app,db,celery
from app import create_app,db
#from flask_script import Manager
#from flask_mail import Mail

 
app = create_app()
app.debug = True
#mail = Mail(app)


CSRF_ENABLED = True
#manager = Manager(app)
 
#@manager.shell
def make_shell_context():
    return dict(app=app,db=db)


#@manager.command
def test():
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

def run_shell():
    #manager.run()
    pass

def run_main():
    try:
        db.create_all(app=app)
        print('-------------')
        print (' the web site is : ')
        print("http://1.14.160.227:7000")
        print('-------------')
        app.run(host='0.0.0.0', port=7000, debug=True)
    except Exception as e:
        print('create table wrong')
        print (e)
if __name__ == '__main__':
    #print(app.config)
    run_main()

    #run_shell()

