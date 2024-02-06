from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from services.wikiWordCount.routes.api import api_bp
from middleware import log_requests

db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(api_bp, url_prefix='/api')

    log_requests(app)

    return app
