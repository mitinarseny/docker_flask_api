from datetime import timedelta

from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_refresh_token_required)
from flask_restplus import (Resource, reqparse, fields, Model, marshal_with)

from . import api

auth = api.namespace('auth', description='Auth')

parser = reqparse.RequestParser()
parser.add_argument('username',
                    type=str,
                    location='json',
                    required=True,
                    nullable=False)
parser.add_argument('password',
                    type=str,
                    location='json',
                    required=True,
                    nullable=False)

REFRESH_TOKEN_EXPIRES_IN = timedelta(days=365)
ACCESS_TOKEN_EXPIRES_IN = timedelta(hours=1)

token_field = {
    'token': fields.String,
    'expire_in': fields.Integer
}


@auth.route('/')
class Auth(Resource):
    @marshal_with(Model('auth_response', {
        'access_token': fields.Nested(token_field),
        'refresh_token': fields.Nested(token_field)
    }))
    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        # find user
        user_id = 123
        return {
                   'access_token': {
                       'token': create_access_token(user_id, expires_delta=ACCESS_TOKEN_EXPIRES_IN),
                       'expire_in': ACCESS_TOKEN_EXPIRES_IN.total_seconds()
                   },
                   'refresh_token': {
                       'token': create_refresh_token(user_id, expires_delta=REFRESH_TOKEN_EXPIRES_IN),
                       'expire_in': REFRESH_TOKEN_EXPIRES_IN.total_seconds()
                   },
               }, 200


@auth.route('/refresh')
class RefreshToken(Resource):
    method_decorators = [jwt_refresh_token_required]

    @marshal_with(Model('refresh_response', {
        'access_token': fields.Nested(token_field)
    }))
    def post(self):
        identity = get_jwt_identity()
        return {
                   'access_token': {
                       'token': create_access_token(identity=identity, expires_delta=REFRESH_TOKEN_EXPIRES_IN),
                       'expire_in': REFRESH_TOKEN_EXPIRES_IN.total_seconds()
                   }
               }, 200
