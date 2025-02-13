import unittest
from flask_app import app, analyze  # Ensure your script is named 'app.py' or adjust accordingly

class AppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_analyze_positive(self):
        response = self.app.post('/analyze', json={'msg': 'amazing product'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['sentiment'], "positive")
        self.assertEqual(data['body_color'], "bg-success")

    def test_analyze_negative(self):
        response = self.app.post('/analyze', json={'msg': 'terrible experience'})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['sentiment'], "negative")
        self.assertEqual(data['body_color'], "bg-danger")

    def test_analyze_empty(self):
        response = self.app.post('/analyze', json={'msg': ''})
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['sentiment'], "none")
        self.assertEqual(data['body_color'], "bg-dark")

if __name__ == "__main__":
    unittest.main()
