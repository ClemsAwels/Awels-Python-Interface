import unittest
import requests
from unittest.mock import patch, Mock
from services.admin import AdminService
import os

# app/services/test_admin.py

class TestAdminService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.admin_service = AdminService()
        cls.base_url = os.getenv("BASE_URL")
        cls.token = os.getenv("TOKEN")
        cls.id_user = None

    @patch('requests.request')
    def test_handle_request_successful(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {"message": "Success"}
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        response, status_code = self.admin_service.handle_request("GET", self.base_url, self.token)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, {"message": "Success"})

    @patch('requests.request')
    def test_handle_request_http_error_with_valid_json(self, mock_request):
        mock_response = Mock()
        mock_response.json.return_value = {"message": "Invalid request"}
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("400 Client Error")
        mock_request.return_value = mock_response

        response, status_code = self.admin_service.handle_request("GET", self.base_url, "invalid_token")
        self.assertEqual(status_code, 400)
        self.assertEqual(response, {"error": "HTTP Error: Invalid request"})

    @patch('requests.request')
    def test_handle_request_http_error_with_invalid_json(self, mock_request):
        mock_response = Mock()
        mock_response.json.side_effect = ValueError("Invalid JSON")
        mock_response.text = "Invalid JSON response"
        mock_response.status_code = 500
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError("500 Server Error")
        mock_request.return_value = mock_response

        response, status_code = self.admin_service.handle_request("GET", self.base_url, "invalid_token")
        self.assertEqual(status_code, 500)
        self.assertEqual(response, {"error": "HTTP Error: Invalid JSON response"})

    @patch('requests.request')
    def test_handle_request_connection_error(self, mock_request):
        mock_request.side_effect = requests.exceptions.RequestException("Connection error")

        response, status_code = self.admin_service.handle_request("GET", self.base_url, self.token)
        self.assertEqual(status_code, 500)
        self.assertEqual(response, {"error": "Request failed: Connection error"})

    @patch('requests.get')
    def test_is_multi_user_mode(self, mock_get):
        mock_response = Mock()
        mock_response.json.return_value = {"isMultiUser": True}
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        response, status_code = self.admin_service.is_multi_user_mode(self.token)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, {"isMultiUser": True})

    @patch('requests.post')
    def test_create_user(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1, "username": "newuser"}
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        response, status_code = self.admin_service.create_user("newuser", "password", "default", self.token)
        self.assertEqual(status_code, 200)
        self.assertIn("id", response["user"])
        self.assertEqual(response["user"]["username"], "newuser")
        TestAdminService.id_user = response["user"]["id"]

    @patch('requests.post')
    def test_update_user(self, mock_post):
        mock_response = Mock()
        mock_response.json.return_value = {"id": 1, "username": "updateduser"}
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        response, status_code = self.admin_service.update_user(TestAdminService.id_user, username="updateduser", token=self.token)
        self.assertEqual(status_code, 200)
        

    @patch('requests.delete')
    def test_delete_user(self, mock_delete):
        mock_response = Mock()
        mock_response.json.return_value = {"message": "User deleted"}
        mock_response.status_code = 200
        mock_response.raise_for_status.return_value = None
        mock_delete.return_value = mock_response

        response, status_code = self.admin_service.delete_user(TestAdminService.id_user, self.token)
        self.assertEqual(status_code, 200)
        self.assertEqual(response, {'success': True, 'error': None})


if __name__ == '__main__':
    unittest.main()