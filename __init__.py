from flask import Flask, jsonify
from .routes import home_bp,admin_bp,auth_bp
from .routes import test_bp
from .config import BaseConfig



def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.secret_key = BaseConfig.SECRET_KEY
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)

    app.register_blueprint(test_bp)

    # @app.route('/')
    # def hello():
    #     return 'Hey there!'

    
 
    return app
