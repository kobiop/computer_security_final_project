from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_cors import CORS
from flask_mail import Mail
from datetime import timedelta
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

mail = Mail()
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Load configuration from environment variables
    app.secret_key = os.getenv("SECRET_KEY")

    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("SQLALCHEMY_DATABASE_URI")

    app.config["MAIL_SERVER"] = os.getenv("MAIL_SERVER")
    app.config["MAIL_PORT"] = int(os.getenv("MAIL_PORT"))  # Convert to integer
    app.config["MAIL_USE_TLS"] = os.getenv("MAIL_USE_TLS") == "True"
    app.config["MAIL_USE_SSL"] = os.getenv("MAIL_USE_SSL") == "True"
    app.config["MAIL_USERNAME"] = os.getenv("MAIL_USERNAME")
    app.config["MAIL_PASSWORD"] = os.getenv("MAIL_PASSWORD")
    app.config["MAIL_DEFAULT_SENDER"] = os.getenv("MAIL_DEFAULT_SENDER")

    app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
        minutes=int(os.getenv("PERMANENT_SESSION_LIFETIME"))
    )

    mail.init_app(app)
    db.init_app(app)

    CORS(
        app,
        resources={r"/*": {"origins": os.getenv("CORS_ORIGINS")}},
        supports_credentials=True,
    )

    app.config["SESSION_COOKIE_SAMESITE"] = os.getenv("SESSION_COOKIE_SAMESITE")

    from .auth import auth
    from .view import view

    app.register_blueprint(auth, url_prefix="/")
    app.register_blueprint(view, url_prefix="/")

    return app
