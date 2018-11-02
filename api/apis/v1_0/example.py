from flask_jwt_extended import (jwt_required,
                                get_jwt_identity)
from flask_restplus import (Resource,
                            reqparse,
                            fields,
                            Model,
                            marshal_with)

from . import api

example = api.namespace('example', description='Example Description')

parser = reqparse.RequestParser()
parser.add_argument('field1',
                    type=str,
                    location='json',
                    required=True,
                    nullable=False)
parser.add_argument('field2',
                    type=int,
                    location='json',
                    required=True,
                    nullable=False)

simple_response = {
    'response': fields.String
}


@example.route('/')
class Example(Resource):
    method_decorators = [jwt_required]

    @marshal_with(Model('example_get', simple_response))
    def get(self):
        user_id = get_jwt_identity()
        # do sth
        return {
                   'response': 'Hello, World!'
               }, 200

    @marshal_with(Model('example_get', simple_response))
    def post(self):
        user_id = get_jwt_identity()
        args = parser.parse_args()
        field1 = args['field1']
        field2 = args['field2']
        # do sth
        return {
                   'response': 'Hello, World!'
               }, 200
