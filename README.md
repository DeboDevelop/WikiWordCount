# WikiWordCount

My submission uses Flask and PostgreSQL to create a set of APIs structured according to service-oriented architecture. For word analysis, it employs dictionaries to track word counts and a priority queue to extract the top N words. Past search results are stored and retrieved from PostgreSQL using a paginated API. Additionally, I've added an optional blacklisting feature, controlled by a feature flag, allowing users to exclude specific words (not part of the original requirements). The system also supports adding new words to the blacklist.

## Project Setup

Create a Virtual Environment (Recommended):
```
python -m venv venv
```
Activate the virtual environment:

On Linux/macOS
```
source venv/bin/activate
```

On Windows
```
venv\Scripts\activate
```

Install dependencies:
```
pip install -r requirements.txt
```

Create and set up .env file:

Create a file named .env in the src directory.
Add necessary environment variables following the format KEY=VALUE, for example:

```
FLASK_ENV=dev
SQLALCHEMY_DATABASE_URI=postgresql://username:password@localhost/db_name
SQLALCHEMY_TEST_DATABASE_URI=postgresql://username:password@localhost/db_name_test
```

Set up database:

Create a PostgreSQL database with the name specified in SQLALCHEMY_DATABASE_URI and SQLALCHEMY_TEST_DATABASE_URI.

Run the application:
```
python run.py
```

Run the unit test:
```
python -m unittest discover -s tests
```
This will start the Flask development server at [http://localhost:5000](http://localhost:5000) by default.

Open Flasgger Docs:
[http://localhost:5000/apidocs/](http://localhost:5000/apidocs/)

## Documentation

API documentation and endpoints are generated using Flasgger. Consider using tools like Postman or Swagger UI to explore and test the API. Unfortunately, due to issues with Flasgger (details [here](https://github.com/flasgger/flasgger/issues/405)), we are unable to include example requests and responses. However, we have provided example requests and responses below for your reference.

Word Frequency:
GET /api/word-frequency?topic=India&n=10
```
[
  {
    "count": 444,
    "word": "of"
  },
  {
    "count": 298,
    "word": "in"
  },
  {
    "count": 197,
    "word": "to"
  },
  {
    "count": 148,
    "word": "India"
  }
]

```

Search:
GET /api/search?page=29&per_page=1
```
{
  "pagination": {
    "current_page": 29,
    "per_page": 1,
    "total_entries": 29,
    "total_pages": 29
  },
  "search_history": [
    {
      "n": 4,
      "timestamp": "2024-02-07 23:32:52",
      "top_words": [
        {
          "count": 444,
          "word": "of"
        },
        {
          "count": 298,
          "word": "in"
        },
        {
          "count": 197,
          "word": "to"
        },
        {
          "count": 148,
          "word": "India"
        }
      ],
      "topic": "India"
    }
  ]
}
```
