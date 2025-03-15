from flask import Flask
from .routes import bp
from os import getenv

secret_key = getenv('FLASK_SECRET_KEY')

def create_app():
    app = Flask(__name__)
    app.secret_key = secret_key
    app.register_blueprint(bp)
    return app