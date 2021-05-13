
from flask import Flask
from flask_restful import Resource, Api, reqparse
import ast
import helpers...

app = Flask(__name__)
api = Api(app)


class ListSort(Resource):
    def get(self):

        return {'data': data}, 200

    def post(self):
        return 404


api.add_resource(ListSort, '/listsort')  # '/users' is our entry point for Users


if __name__ == '__main__':
    app.run()  # run our Flask app
