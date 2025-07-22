from flask import Flask
from os import getenv
from dotenv import load_dotenv
load_dotenv()
from .routes.auth import auth_bp
from .routes.transaction import transaction_bp
from .routes.relatory import relatory_bp
from flask_jwt_extended import JWTManager
from .config.jwt_handlers import setup_jwt_handlers


from db import db


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = getenv('SECRET_KEY', 'dev-secret-key')
    app.config['JWT_SECRET_KEY'] = getenv('JWT_SECRET_KEY', 'dev-jwt-secret-key')
    jwt = JWTManager(app)
    setup_jwt_handlers(jwt)
    

    app.config['SQLALCHEMY_DATABASE_URI'] = getenv('DATABASE_URL', 'sqlite:///db.sqlite3')
    db.init_app(app)


    app.register_blueprint(auth_bp)
    app.register_blueprint(transaction_bp)
    app.register_blueprint(relatory_bp)


    with app.app_context():
        db.create_all()

    return app