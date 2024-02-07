from typing import Optional
from flask import request

from services.wikiWordCount.models.search import Search
from services.wikiWordCount.word_frequency import get_word_frequency

from utils.logger import logger
from utils.db import db


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

def search_history_controller() -> dict:
    try:
        # Get page and per_page parameters from the request or use defaults
        page = request.args.get('page', default=1, type=int)
        per_page = request.args.get('per_page', default=10, type=int)

        # Paginate the search history
        search_history = Search.query.paginate(page=page, per_page=per_page)

        # Format the paginated search history for response
        formatted_history = [
            {
                'topic': entry.topic,
                'n': entry.n,
                'top_words': entry.top_words,
                'timestamp': entry.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            }
            for entry in search_history.items
        ]

        # Create pagination metadata
        pagination_metadata = {
            'total_pages': search_history.pages,
            'current_page': search_history.page,
            'total_entries': search_history.total,
            'per_page': per_page
        }

        # Return the paginated result along with pagination metadata
        response_data = {
            'search_history': formatted_history,
            'pagination': pagination_metadata
        }

        return response_data
    except Exception as e:
        logger.error(f"Error retrieving paginated search history: {str(e)}")
        return {'error': 'Internal Server Error'}, 500