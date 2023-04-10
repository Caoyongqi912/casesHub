# @Time : 2023/4/10 22:02 
# @Author : cyq
# @File : userSwagger.py 
# @Software: PyCharm
# @Desc:


my_custom_operation = {
    'notes': '添加管理员',
    'parameters': [
        {
            "name": "username",
            "description": "管理员名称",
            "required": True,
            "type": "string",
            "paramType": "body"
        },
        {
            "name": "password",
            "description": "管理员密码",
            "required": True,
            "type": "string",
            "paramType": "body"
        },
        {
            "name": "phone",
            "description": "电话",
            "required": True,
            "type": "string",
            "paramType": "body"
        },
    ],
    'responseMessages': [
        {
            "code": 200,
            "message": "Success"
        },
        {
            "code": 400,
            "message": "Bad request"
        }
    ]
}
