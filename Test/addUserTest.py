# @Time : 2022/7/12 20:11 
# @Author : cyq
# @File : addUserTest.py 
# @Software: PyCharm
# @Desc:
import random
import unittest
from faker import Faker

from App import create_app

f = Faker()
app = create_app()


class AddUserTest(unittest.TestCase):

    def setUp(self) -> None:
        app.testing = True
        self.username = "admin"
        self.password = "admin"
        self.body = {
            "username": f.name(),
            "password": f.pystr(),
            "phone": f.phone_number(),
            "email": f.email(),
            "gender": random.choices(["MALE", "FEMALE"]),
            "isAdmin": True,
            "tag": random.choices(["QA", "PR", "DEV"])

        }
        self.client = app.test_client()

    def test_addUsers(self):
        for i in range(100):
            resp = app.test_client().post("/v1/api/user/addUser",
                                          json=self.body).json
