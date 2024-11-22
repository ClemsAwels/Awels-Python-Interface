import unittest
from services.admin import AdminService
from services.authentification import AuthentificationService
import os
from dotenv import load_dotenv

class TestAdminService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        load_dotenv()
        cls.token = os.getenv("TOKEN")
        cls.admin_service = AdminService(auth_service=AuthentificationService())

    def test_is_multi_user_mode(self):
        response, status_code = self.admin_service.is_multi_user_mode(self.token)
        self.assertEqual(status_code, 200)
        self.assertIn("multiUserMode", response)

    def test_list_users(self):
        response, status_code = self.admin_service.list_users(self.token)
        self.assertEqual(status_code, 200)
        self.assertIsInstance(response, list)

    def test_create_user(self):
        response, status_code = self.admin_service.create_user("testuser", "password", "user", self.token)
        self.assertEqual(status_code, 201)
        self.assertIn("id", response)

    def test_update_user(self):
        user_id = "testuser_id"  # La méthode doit être activée sur le serveur pour fonctionner
        response, status_code = self.admin_service.update_user(user_id, username="updateduser", token=self.token)
        self.assertEqual(status_code, 200)
        self.assertIn("username", response)

    def test_delete_user(self):
        user_id = "testuser_id"  # La méthode doit être activée sur le serveur pour fonctionner
        response, status_code = self.admin_service.delete_user(user_id, self.token)
        self.assertEqual(status_code, 200)
        self.assertIn("message", response)

    def test_list_invites(self):
        response, status_code = self.admin_service.list_invites(self.token)
        self.assertEqual(status_code, 200)
        self.assertIsInstance(response, list)

    def test_create_invite(self):
        workspace_ids = ["workspace_id"]  # Remplacez par des IDs de workspace valides
        response, status_code = self.admin_service.create_invite(workspace_ids, self.token)
        self.assertEqual(status_code, 201)
        self.assertIn("id", response)

    def test_deactivate_invite(self):
        invite_id = "invite_id"  # Remplacez par un ID d'invitation valide
        response, status_code = self.admin_service.deactivate_invite(invite_id, self.token)
        self.assertEqual(status_code, 200)
        self.assertIn("message", response)

if __name__ == '__main__':
    unittest.main()