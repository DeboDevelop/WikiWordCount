from flask import Flask
from config import Config
from services.wikiWordCount.routes.api import api_bp
from middleware import log_requests
from services.wikiWordCount.models.search import Search
from utils.db import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api_bp, url_prefix='/api')

    log_requests(app)

    return app
