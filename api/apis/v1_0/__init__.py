from flask import Blueprint
from flask_jwt_extended import JWTManager
from flask_restplus import Api, apidoc

api_bp = Blueprint('api', __name__)
authorizations = {
    'Bearer': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
api = Api(api_bp,
          version='1.0',
          authorizations=authorizations,
          doc='/doc/',
          title='A Simple API',
          description='Simple API Documentation')
jwt = JWTManager()
jwt._set_error_handler_callbacks(api)
from . import (
    auth,
    example
)

# Use it to export documentation
API_DOCS_DIR = 'swagger_docs'
from flask import json


@api.documentation
def export_docs():
    api_version = '.'.join(__name__.rsplit('.', 1)[-1].split('_'))
    with open(f'{API_DOCS_DIR}/{api_version}.json', 'w+') as f:
        f.write(json.dumps(api.__schema__))
    return apidoc.ui_for(api)
