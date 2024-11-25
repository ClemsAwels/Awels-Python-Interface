import requests
import os
from dotenv import load_dotenv
from .authentification import AuthentificationService

class AdminService:
    def __init__(self, auth_service=None):
        load_dotenv()
        self.auth_service = auth_service or AuthentificationService()
        self.base_url = os.getenv("BASE_URL")

    def handle_request(self, method, url, token, **kwargs):
        """
        Gère les requêtes HTTP pour les méthodes du service.
        """
        headers = {"Authorization": f"Bearer {token}"}
        try:
            response = requests.request(method, url, headers=headers, **kwargs)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as e:
            try:
                error_details = response.json()
                error_message = error_details.get("message", str(error_details))
            except ValueError:
                error_message = response.text
            return {"error": f"HTTP Error: {error_message}"}, response.status_code
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}, 500

    def is_multi_user_mode(self, token):
        """
        GET /v1/admin/is-multi-user-mode
        Vérifie si l'instance est en mode multi-utilisateur.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/admin/is-multi-user-mode"
        return self.handle_request("GET", url, token)

    def list_users(self, token):
        """
        GET /v1/admin/users
        Récupère la liste de tous les utilisateurs en mode multi-utilisateur.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/admin/users"
        return self.handle_request("GET", url, token)

    def create_user(self, username, password, role, token):
        """
        POST /v1/admin/users/new
        Crée un nouvel utilisateur avec un nom d'utilisateur, un mot de passe et un rôle.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/admin/users/new"
        data = {
            "username": username,
            "password": password,
            "role": role
        }
        return self.handle_request("POST", url, token, json=data)

    def update_user(self, user_id, username=None, password=None, role=None, suspended=None, token=None):
        """
        POST /v1/admin/users/{id}
        Met à jour les informations d'un utilisateur spécifique.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/admin/users/{user_id}"
        data = {k: v for k, v in {
            "username": username,
            "password": password,
            "role": role,
            "suspended": suspended
        }.items() if v is not None}
        return self.handle_request("POST", url, token, json=data)

    def delete_user(self, user_id, token):
        """
        DELETE /v1/admin/users/{id}
        Supprime un utilisateur par son identifiant.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/admin/users/{user_id}"
        return self.handle_request("DELETE", url, token)

    def list_invites(self, token):
        """
        GET /v1/admin/invites
        Liste toutes les invitations existantes.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/admin/invites"
        return self.handle_request("GET", url, token)

    def create_invite(self, workspace_ids, token):
        """
        POST /v1/admin/invite/new
        Crée une nouvelle invitation pour enregistrer un utilisateur dans l'instance.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/admin/invite/new"
        data = {"workspaceIds": workspace_ids}
        return self.handle_request("POST", url, token, json=data)

    def deactivate_invite(self, invite_id, token):
        """
        DELETE /v1/admin/invite/{id}
        Désactive une invitation par son identifiant.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/admin/invite/{invite_id}"
        return self.handle_request("DELETE", url, token)
