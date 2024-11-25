import unittest
import requests
from unittest.mock import patch, Mock
from services.authentification import AuthentificationService

# app/test/test_authentification.py

class TestAuthentificationService(unittest.TestCase):
    def setUp(self):
        self.auth_service = AuthentificationService()

    @patch('requests.get')
    def test_no_authorization_token(self, mock_get):
        response, status_code = self.auth_service.auth()
        self.assertEqual(status_code, 403)
        self.assertEqual(response, {"error": "No authorization token provided."})

    @patch('requests.get')
    def test_successful_authentication(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"message": "Success"}
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response, status_code = self.auth_service.auth(Authorization="Bearer valid_token")
        self.assertEqual(status_code, 200)
        self.assertEqual(response, {"message": "Success"})

    @patch('requests.get')
    def test_http_error_with_valid_json(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"message": "Invalid API Key"}
        mock_response.status_code = 403
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("403 Client Error")
        mock_get.return_value = mock_response

        response, status_code = self.auth_service.auth(Authorization="Bearer invalid_token")
        self.assertEqual(status_code, 403)
        self.assertEqual(response, {"error": "Invalid API Key: Invalid API Key"})

    @patch('requests.get')
    def test_http_error_with_invalid_json(self, mock_get):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "Invalid JSON response"
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
        mock_get.return_value = mock_response

        response, status_code = self.auth_service.auth(Authorization="Bearer invalid_token")
        self.assertEqual(status_code, 500)
        self.assertEqual(response, {"error": "Authentication service error: Invalid JSON response"})

    @patch('requests.get')
    def test_connection_error(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Connection error")

        response, status_code = self.auth_service.auth(Authorization="Bearer valid_token")
        self.assertEqual(status_code, 500)
        self.assertEqual(response, {"error": "Failed to connect to the authentication service: Connection error"})

if __name__ == '__main__':
    unittest.main()