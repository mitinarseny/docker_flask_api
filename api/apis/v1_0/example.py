from flask_jwt_extended import (jwt_required,
                                get_jwt_identity)
from flask_restplus import (Resource,
                            fields)

from . import api

ns = api.namespace('example', description='Example Description', decorators=[jwt_required])

example_response = ns.model(
    name='Example Response',
    model={
        'response': fields.String(
            example='Example Response'
        )
    }
)


@ns.response(401, 'Unauthorized')
@ns.route('/')
class Example(Resource):
    method_decorators = [jwt_required]

    post_parser = ns.parser()
    post_parser.add_argument('field1',
                             type=str,
                             location='json',
                             required=True,
                             nullable=False)
    post_parser.add_argument('field2',
                             type=int,
                             location='json',
                             required=True,
                             nullable=True)

    @ns.marshal_with(example_response)
    def get(self):
        user_id = get_jwt_identity()

        # do sth

        return {
                   'response': 'Hello, World!'
               }, 200

    @ns.expect(ns.model(
        name='Example Request',
        model={
            'field1': fields.String(
                required=True,
                description='field1 description',
                example='Example1'),
            'field2': fields.String(
                required=True,
                description='field2 description',
                example='Example2')
        }
    ))
    @ns.marshal_with(example_response)
    def post(self):
        user_id = get_jwt_identity()

        args = self.post_parser.parse_args()

        field1 = args['field1']
        field2 = args['field2']

        # do sth

        return {
                   'response': 'Hello, World!'
               }, 200
