from flask import Flask
from config import Config
from flasgger import Swagger

from services.wikiWordCount.routes.api import api_bp
from services.wikiWordCount.models.search import Search

from middleware import log_requests

from utils.db import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(api_bp, url_prefix='/api')

    log_requests(app)

    swagger = Swagger(app)

    return app
