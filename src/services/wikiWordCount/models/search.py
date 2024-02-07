from sqlalchemy.sql import func

from utils.db import db

class Search(db.Model):
    __tablename__ = 'searches'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column(db.String, nullable=False)
    n = db.Column(db.Integer, nullable=False)
    top_words = db.Column(db.JSON, nullable=True)
    timestamp = db.Column(db.DateTime(timezone=True), server_default=func.now(), nullable=False)
