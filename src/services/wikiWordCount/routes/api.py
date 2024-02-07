from flask import Blueprint

from services.wikiWordCount.controllers.wikipedia_controller import word_frequency_controller, search_history_controller

api_bp = Blueprint('api', __name__)

api_bp.route('/word-frequency', methods=['GET'])(word_frequency_controller)
api_bp.route('/search', methods=['GET'])(search_history_controller)