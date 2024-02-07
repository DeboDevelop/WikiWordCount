from typing import Optional
from flask import request

from services.wikiWordCount.models.search import Search
from services.wikiWordCount.word_frequency import get_word_frequency

from utils.logger import logger
from utils.db import db


def word_frequency_controller() -> dict:
    """ This endpont is used to get top n words by word count in a wikipedia article.
    ---
    summary: "Analyze wikipedia article"
    description: "Analyze wikipedia article based on word count and return top n words"
    produces:
      - "application/json"
    parameters:
      - name: topic
        in: query
        type: string
        required: true
        default: None
        description: Name of the topic
      - name: n
        in: query
        type: integer
        required: false
        default: 10
        description: Number of top words required
    responses:
      200:
        description: A list of words and their counts
        schema:
          type: "array"
          items:
            $ref: '#/definitions/WordCount'
      400:
        description: Invalid input
        schema:
          type: "object"
          properties:
            error:
              type: string
      500:
        description: Internal Server Error
        schema:
          type: "object"
          properties:
            error:
              type: string
    definitions:
      WordCount:
        type: object
        properties:
          word:
            type: string
          count:
            type: integer
    """
    try:
        n_param = request.args.get('n', default='10')
        # Check if 'n' is a valid integer
        try:
            n = int(n_param)
        except ValueError:
            return {'error': 'Invalid value for n, must be an integer'}, 400
        
        topic: Optional[str] = request.args.get('topic')

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
    """ This endpont is used to list previous word frequency analysis result.
    ---
    summary: "List Past Result"
    description: "Paginated API to list past results"
    produces:
      - "application/json"
    parameters:
      - name: page
        in: query
        type: integer
        required: true
        default: 1
        description: Page Number 
      - name: per_page
        in: query
        type: integer
        required: true
        default: 10
        description: Amount of data requested per page
    responses:
      200:
        description: A list of previous search results
        schema:
          type: "array"
          items:
            $ref: '#/definitions/SearchHistory'
      400:
        description: Invalid input
        schema:
          type: "object"
          properties:
            error:
              type: string
      500:
        description: Internal Server Error
        schema:
          type: "object"
          properties:
            error:
              type: string
    definitions:
      SearchHistory:
        type: "object"
        properties:
          search_history:
            type: "object"
            items:
              $ref: '#/definitions/SearchHistoryItem'
          pagination:
            type: "object"
            items:
              $ref: '#/definitions/PaginateObject'
      SearchHistoryItem:
        type: "object"
        properties:
          topic:
            type: string
          n:
            type: integer
          top_words:
            type: "array"
            items:
              $ref: '#/definitions/WordCount'
          timestamp:
            type: "datetime"
      PaginateObject:
        type: "object"
        properties:
          page:
            type: integer
          per_page:
            type: integer
    """
    try:
        # Attempt to get the values of 'page' and 'per_page' from the request args
        page_param = request.args.get('page', default='1')
        per_page_param = request.args.get('per_page', default='10')
        try:
            page = int(page_param)
        except ValueError:
            return {'error': 'Invalid value for page, must be an integer'}, 400

        try:
            per_page = int(per_page_param)
        except ValueError:
            return {'error': 'Invalid value for per_page, must be an integer'}, 400

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