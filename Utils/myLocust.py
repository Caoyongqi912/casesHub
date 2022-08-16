# @Time : 2022/8/16 20:22 
# @Author : cyq
# @File : myLocust.py 
# @Software: PyCharm
# @Desc:


from locust import HttpUser, task
from faker import Faker
from random import randint

f = Faker()


class MyLocust(HttpUser):

    def on_start(self):
        self.body = {
            "title": "case" + f.pystr()[:5],
            "desc": f.pystr(),
            "setup": "我是前置" + f.pystr(),
            "tag": randint(1, 2),
            "case_level": randint(1, 4),
            "platformID": randint(1, 2),
            "projectID": randint(1, 4),
            "partID": randint(1, 18),
            "versionID": randint(1, 2),
            "info": [
                {
                    "step": 1,
                    "do": "xxx",
                    "exp": "xxx"
                },
                {
                    "step": 2,
                    "do": "xxx",
                    "exp": "xxxx"
                }
            ]
        }
        print("start")

    def on_stop(self):
        print("step")

    @task
    def addCase(self):
        url = "/api/case/opt"
        self.client.post(url, json=self.body, auth=("dawa", "dawa"))


if __name__ == "__main__":
    import os

    os.system("locust -f myLocust.py --host=http://localhost:5000")
