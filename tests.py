import unittest
from app import app
from serializer import COMPONENTS, OrderSerializer

class TestOrderAPI(unittest.TestCase):
    """Test the orders API endpoint."""
    def setUp(self):
        """Set up test environment."""
        self.app = app.test_client()
        self.app.testing = True
        
    def test_create_valid_order(self):
        """Test creating order with all required categories"""
        test_data = {
            "components": ["A", "D", "F", "I", "K"]
        }
        response = self.app.post('/orders', json=test_data)
        # Check response status code
        self.assertEqual(response.status_code, 201)
        
        # Check response data
        data = response.get_json()
        self.assertIn('order_id', data)
        self.assertIn('total', data)
        self.assertIn('parts', data)
        expected_total = sum(COMPONENTS[code].price for code in test_data['components'])
        self.assertEqual(data['total'], round(expected_total, 2))
        self.assertEqual(len(data['parts']), 5)

    def test_missing_category(self):
        """Test order creation with missing required category"""
        test_data = {
            "components": ["A", "D", "F", "I"]
        }
        response = self.app.post('/orders', json=test_data)
        # Check response status code
        self.assertEqual(response.status_code, 400)
        
        # Check response data
        data = response.get_json()
        self.assertEqual(data['error'], "Missing components for categories: 'Body'")
        
    def test_duplicate_category(self):
        """Test order with duplicate component categories"""
        test_data = {
            "components": ["A", "B", "D", "F", "I", "K"]
        }
        response = self.app.post('/orders', json=test_data)
        # Check response status code
        self.assertEqual(response.status_code, 400)
        
        # Check response data
        data = response.get_json()
        self.assertEqual(data['error'], "Duplicate component for category: 'Screen'")

    def test_duplicate_component_codes(self):
        """Test order with duplicate component codes"""
        test_data = {
            "components": ["A", "A", "D", "F", "F", "K"]
        }
        response = self.app.post('/orders', json=test_data)
        # Check response status code
        self.assertEqual(response.status_code, 400)
        
        # Check response data
        data = response.get_json()
        self.assertEqual(data['error'], "Duplicate component codes found: 'A, F'")

    def test_invalid_component_code(self):
        """Test order with invalid component code"""
        test_data = {
            "components": ["A", "D", "F", "I", "Z"]
        }
        response = self.app.post('/orders', json=test_data)
        # Check response status code
        self.assertEqual(response.status_code, 400)
        
        # Check response data
        data = response.get_json()
        self.assertEqual(data['error'], "Invalid component code: 'Z'")

    def test_invalid_components_type(self):
        """Test order with non-list components"""
        test_data = {
            "components": "not_a_list"
        }
        response = self.app.post('/orders', json=test_data)
        # Check response status code
        self.assertEqual(response.status_code, 400)
        
        # Check response data
        data = response.get_json()
        self.assertEqual(data['error'], "'Components' must be a list.")

if __name__ == '__main__':
    unittest.main()