import unittest 
from flask_app import app 

class AppTestCase(unittest.TestCase): 
    def setUp(self): 
        self.app = app.test_client() 
        self.app.testing = True 

    def test_app(self): 
        response = self.app.get('/') 
        self.assertEqual(response.status_code, 200) 
        
if __name__ == '__main__': 
    unittest.main() 