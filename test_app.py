import unittest
import json
from app import app

class FlaskAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_add_numbers_success(self):
        response = self.app.post('/add', 
            data=json.dumps({'num1': 10, 'num2': 20}),
            content_type='application/json')
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['sum'], 30)

    def test_add_numbers_missing_param(self):
        response = self.app.post('/add', 
            data=json.dumps({'num1': 10}),
            content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)

    def test_add_numbers_invalid_param(self):
        response = self.app.post('/add', 
            data=json.dumps({'num1': 'abc', 'num2': 20}),
            content_type='application/json')

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', data)

if __name__ == "__main__":
    unittest.main()