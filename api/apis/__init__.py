import os


def add_apis(app):
    app.config['BUNDLE_ERRORS'] = os.environ['BUNDLE_API_ERRORS']
    app.config['JWT_SECRET_KEY'] = os.environ['JWT_SECRET_KEY']

    from . import v1_0
    app.register_blueprint(v1_0.api_bp, url_prefix='/api/v1.0')
    v1_0.jwt.init_app(app)
