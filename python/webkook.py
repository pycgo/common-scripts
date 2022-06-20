'''
接收prometheus 发的webhoook数据 用来测试数据样例
'''
import json
from flask import Flask, request
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    prometheus_data = json.loads(request.data)
    print(prometheus_data)
    return "test"
    
if __name__ == '__main__':
    WSGIServer(('0.0.0.0', 5000), app).serve_forever()
