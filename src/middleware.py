# middleware.py
from flask import request
from utils.logger import logger

def log_requests(app):
    @app.before_request
    def log_request_info():
        logger.info(f'Request: {request.method} {request.path}')

