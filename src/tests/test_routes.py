import unittest
from app import create_app
from utils.db import db
from config import TestConfig

topic = 'python'

class TestSearchHistoryAndWordFrequencyRoutes(unittest.TestCase):
    def setUp(self):
        app = create_app(config_class=TestConfig)
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with self.client.application.app_context():
            db.drop_all()
    
    def test_word_frequency_route(self):
        # Test typical use case
        with self.client.get(f'/api/word-frequency?topic={topic}&n=10') as response:
            self.assertEqual(response.status_code, 200)
            data = response.get_json()

            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 10)
        
        # Test invalid topic (non-existent Wikipedia page)
        with self.client.get('/api/word-frequency?topic=InvalidTopic&n=5') as response:
            self.assertEqual(response.status_code, 400)

        # Test invalid parameter (non-integer value for n)
        with self.client.get(f'/api/word-frequency?topic={topic}&n=invalid') as response:
            self.assertEqual(response.status_code, 500)

    def test_search_history_route(self):
        response = self.client.get(f'/api/word-frequency?topic={topic}&n=10')

        with self.client.get('/api/search') as response:
            self.assertEqual(response.status_code, 200)
            data = response.get_json()

            # Assert response fields
            self.assertIn('search_history', data)
            self.assertIn('pagination', data)

            # Assert pagination fields
            pagination = data.get('pagination', {})
            self.assertIn('current_page', pagination)
            self.assertIn('per_page', pagination)
            self.assertIn('total_entries', pagination)
            self.assertIn('total_pages', pagination)

            # Assert search history fields
            search_history = data.get('search_history', [])
            self.assertGreater(len(search_history), 0)

            first_entry = search_history[0]
            self.assertIn('n', first_entry)
            self.assertIn('timestamp', first_entry)
            self.assertIn('top_words', first_entry)
            self.assertIn('topic', first_entry)

    

if __name__ == '__main__':
    unittest.main()
