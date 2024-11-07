import requests
import os
from dotenv import load_dotenv
from .authentification import AuthentificationService

class AdminService:
    def __init__(self, auth_service=None):
        load_dotenv()
        self.auth_service = auth_service or AuthentificationService()
        self.base_url = os.getenv("BASE_URL")
        print("AdminService initialisé")

    def is_multi_user_mode(self, token):
        """
        GET /v1/admin/is-multi-user-mode
        Vérifie si l'instance est en mode multi-utilisateur.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/admin/is-multi-user-mode"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to check multi-user mode"}, 500

    def list_users(self, token):
        """
        GET /v1/admin/users
        Récupère la liste de tous les utilisateurs en mode multi-utilisateur.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/admin/users"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to list users"}, 500

    def create_user(self, username, password, role, token):
        """
        POST /v1/admin/users/new
        Crée un nouvel utilisateur avec un nom d'utilisateur, un mot de passe et un rôle.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/admin/users/new"
        headers = {"Authorization": token}
        data = {
            "username": username,
            "password": password,
            "role": role
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to create user"}, 500

    def update_user(self, user_id, username=None, password=None, role=None, suspended=None, token=None):
        """
        POST /v1/admin/users/{id}
        Met à jour les informations d'un utilisateur spécifique.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/admin/users/{user_id}"
        headers = {"Authorization": token}
        data = {k: v for k, v in {
            "username": username,
            "password": password,
            "role": role,
            "suspended": suspended
        }.items() if v is not None}

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to update user"}, 500

    def delete_user(self, user_id, token):
        """
        DELETE /v1/admin/users/{id}
        Supprime un utilisateur par son identifiant.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/admin/users/{user_id}"
        headers = {"Authorization": token}

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to delete user"}, 500

    def list_invites(self, token):
        """
        GET /v1/admin/invites
        Liste toutes les invitations existantes.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/admin/invites"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to list invites"}, 500

    def create_invite(self, workspace_ids, token):
        """
        POST /v1/admin/invite/new
        Crée une nouvelle invitation pour enregistrer un utilisateur dans l'instance.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/admin/invite/new"
        headers = {"Authorization": token}
        data = {
            "workspaceIds": workspace_ids
        }

        try:
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to create invite"}, 500

    def deactivate_invite(self, invite_id, token):
        """
        DELETE /v1/admin/invite/{id}
        Désactive une invitation par son identifiant.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/admin/invite/{invite_id}"
        headers = {"Authorization": token}

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to deactivate invite"}, 500
