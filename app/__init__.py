from flask import Flask
from .routes import bp
from os import getenv

#secret_key = "b01c88a23e2744b3842cb2874e387f5e19e35565b3049dc6990d9215423652a7"
secret_key = getenv('FLASK_SECRET_KEY')

def create_app():
    app = Flask(__name__)
    app.secret_key = secret_key
    app.register_blueprint(bp)
    return app