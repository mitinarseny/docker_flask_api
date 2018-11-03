from datetime import timedelta

from flask_jwt_extended import (create_access_token,
                                create_refresh_token,
                                get_jwt_identity,
                                jwt_refresh_token_required)
from flask_restplus import (Resource,
                            fields)

from . import api, authorizations

ns = api.namespace('auth', description='Auth', authorizations=authorizations)

REFRESH_TOKEN_EXPIRES_IN = timedelta(days=365)
ACCESS_TOKEN_EXPIRES_IN = timedelta(hours=1)

token_model = ns.model('Token', {
    'token': fields.String(
        description='JWT token'),
    'expire_in': fields.Integer(
        description='time in seconds, after which token will expire')
})


@ns.route('/')
class Auth(Resource):
    post_parser = ns.parser()
    post_parser.add_argument('username',
                             type=str,
                             location='json',
                             required=True,
                             nullable=False)
    post_parser.add_argument('password',
                             type=str,
                             location='json',
                             required=True,
                             nullable=False)

    @ns.expect(ns.model(
        name='User',
        model={
            'username': fields.String(
                required=True,
                description='username of the User',
                example='ivan_ivanov'),
            'password': fields.String(
                min_length=8,
                max_length=32,
                example='Qwerty123')
        }
    ))
    @ns.response(400, 'Bad Request')
    @ns.marshal_with(
        fields=ns.model(
            name='Auth',
            model={
                'access_token': fields.Nested(token_model),
                'refresh_token': fields.Nested(token_model)
            }),
        code=200,
        description='Authenticated')
    def post(self):
        args = self.post_parser.parse_args()

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


@ns.route('/refresh')
class RefreshToken(Resource):
    method_decorators = [jwt_refresh_token_required]

    @ns.response(401, 'Unauthorized')
    @ns.marshal_with(
        fields=ns.model(
            name='Refresh Token Response',
            model={
                'access_token': fields.Nested(token_model)
            }),
        code=200,
    )
    def post(self):
        identity = get_jwt_identity()
        return {
                   'access_token': {
                       'token': create_access_token(identity=identity, expires_delta=REFRESH_TOKEN_EXPIRES_IN),
                       'expire_in': REFRESH_TOKEN_EXPIRES_IN.total_seconds()
                   }
               }, 200
