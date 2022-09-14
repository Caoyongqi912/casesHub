# @Time : 2022/7/7 22:48 
# @Author : cyq
# @File : main.py 
# @Software: PyCharm
# @Desc: 入口
from gevent import monkey
from App import create_app
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler

app = create_app()

if __name__ == '__main__':
    # config = Config()
    # app.run(host=config.get_conf("domain", "host"), port=config.get_conf("domain", "port"))
    # celery_cmd = "celery -A celery_task.tasks worker -l info -P eventlet"
    # app.run(host="localhost", port=5000)
    http_server = WSGIServer(("localhost", 5000), app, handler_class=WebSocketHandler)
    http_server.serve_forever()
