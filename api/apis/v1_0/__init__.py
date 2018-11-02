from flask import Blueprint
from flask_jwt_extended import JWTManager
from flask_restplus import Api

api_bp = Blueprint('api', __name__)
api = Api(api_bp)
jwt = JWTManager()
jwt._set_error_handler_callbacks(api)

from . import (
    auth,
    example
)
