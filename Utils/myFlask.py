from flask import Flask
from flask_restx import Resource, Api, Namespace

ns = Namespace('text', description="test desc")
app = Flask(__name__)
api = Api(app)


@api.route('/hello')
@ns.doc("haha")
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


if __name__ == '__main__':
    app.run(debug=True)
    print("哈"*50)