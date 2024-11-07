import requests
import os
from dotenv import load_dotenv
from .authentification import AuthentificationService

class SystemSettingsService:
    def __init__(self, auth_service=None):
        load_dotenv()
        self.auth_service = auth_service or AuthentificationService()
        self.base_url = os.getenv("BASE_URL")
        print("SystemSettingsService initialisé")

    def dump_settings(self, token):
        """
        GET /v1/system/env-dump
        Exporte tous les paramètres actuels vers un fichier de stockage.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/system/env-dump"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to dump settings"}, 500

    def get_system_settings(self, token):
        """
        GET /v1/system
        Récupère tous les paramètres système actuellement définis.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/system"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to get system settings"}, 500

    def get_vector_count(self, token):
        """
        GET /v1/system/vector-count
        Retourne le nombre de vecteurs dans la base de données de vecteurs connectée.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/system/vector-count"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to get vector count"}, 500

    def update_system_setting(self, update_data, token):
        """
        POST /v1/system/update-env
        Met à jour un paramètre ou une préférence du système.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/system/update-env"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, headers=headers, json=update_data)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to update system setting"}, 500

    def export_chats(self, export_type, token):
        """
        GET /v1/system/export-chats
        Exporte toutes les conversations du système dans un format spécifique.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/system/export-chats"
        headers = {"Authorization": token}
        params = {"type": export_type}

        try:
            response = requests.get(url, headers=headers, params=params)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to export chats"}, 500

    def remove_documents(self, document_names, token):
        """
        DELETE /v1/system/remove-documents
        Supprime définitivement des documents spécifiques du système.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/system/remove-documents"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        data = {"names": document_names}

        try:
            response = requests.delete(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to remove documents"}, 500
