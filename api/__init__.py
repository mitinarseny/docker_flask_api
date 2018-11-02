from flask import Flask

app = Flask(__name__)

from .apis import add_apis

add_apis(app)
