from typing import Optional
from flask import request
from services.wikiWordCount.models.search import Search
from utils.logger import logger
from utils.db import db
from services.wikiWordCount.word_frequency import get_word_frequency

def word_frequency_controller() -> dict:
    try:
        topic: Optional[str] = request.args.get('topic')
        n: int = int(request.args.get('n', 10))

        if not topic:
            return {'error': 'Topic name not provided'}, 400

        # Call the function to get word frequency
        result, result_exist = get_word_frequency(topic, n)
        if result_exist:
            new_search = Search(topic=topic, n=n, top_words=result)
            db.session.add(new_search)
            db.session.commit()
            return result
        else:
            return {'error': 'Invalid topic name'}, 400
    except Exception as e:
        logger.error(f"Error processing word frequency request: {str(e)}")
        return {'error': 'Internal Server Error'}, 500