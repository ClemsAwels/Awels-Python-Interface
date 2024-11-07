import requests
import os
from dotenv import load_dotenv
from .authentification import AuthentificationService

class UserManagementService:
    def __init__(self, auth_service=None):
        load_dotenv()
        self.auth_service = auth_service or AuthentificationService()
        self.base_url = os.getenv("BASE_URL")
        print("UserManagementService initialisé")

    def list_users(self, token):
        """
        GET /v1/users
        Récupère la liste de tous les utilisateurs.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/users"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException as e:
            print(f"Erreur de requête : {e}")
            return {"error": "Failed to list users"}, 500
