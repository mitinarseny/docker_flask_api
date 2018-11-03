from flask import Flask
from werkzeug.contrib.fixers import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.url_map.strict_slashes = False


@app.before_first_request
def init():
    from .apis import add_apis
    add_apis(app)
