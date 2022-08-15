# @Time : 2022/7/7 22:48 
# @Author : cyq
# @File : main.py 
# @Software: PyCharm
# @Desc: 入口

from App import create_app

app = create_app()

if __name__ == '__main__':
    # config = Config()
    # app.run(host=config.get_conf("domain", "host"), port=config.get_conf("domain", "port"))
    app.run(host="localhost", port=5000)
