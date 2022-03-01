from flask import Flask
from flask import jsonify,request
import requests
from config import Config
from extensions import logger 


app = Flask(__name__)

@app.route("/t2")
def hello_world():
    print('get a data ')
    #requests.get('192.168.1.202:8000')
    print(request.args)
    print(request.data)
    print(request.get_data())
    return "<p>Hello, World! t2 </p>"

@app.route("/host2server",methods=['POST'])
def host2server():
    ip = request.remote_addr
    print('get a local connect,ip is: '+ip)
    print(ip)
    if ip == f'{Config.LOCAL_HOST_ADDRESS}'.split(':')[0]:
        logger.info(id)
        requests.post(f'http://{Config.REMOTE_SERVER_ADDRESS}/send2server',data=request.data)
    return "<p>Hello, World! t33 </p>"

@app.route("/server2host",methods=['POST'])
def server2host():
    ip = request.remote_addr
    print('get a remote connect,ip is: '+ip)
    if ip == f'{Config.REMOTE_SERVER_ADDRESS}'.split(':')[0]:
        logger.info(ip)
        #logger.info(request.environ.get('HTTP_X_REAL_IP', request.remote_addr) )
        requests.post(f'http://{Config.LOCAL_HOST_ADDRESS}/send2host',data=request.data)
    return "<p>Hello, World! send2host</p>"

@app.route("/update_code",methods=['POST'])
def update_code():
    pass


def configure_logging(app):
    if not os.path.exists('logs'):
        os.mkdir('logs')

if __name__ == '__main__':
    app.run(port=8002,host='0.0.0.0',debug=True)
