import requests
import os
from dotenv import load_dotenv
from .authentification import AuthentificationService

class EmbedService:
    def __init__(self, auth_service=None):
        load_dotenv()
        self.auth_service = auth_service or AuthentificationService()
        self.base_url = os.getenv("BASE_URL")
        print("EmbedService initialisé")

    def list_embeds(self, token):
        """
        GET /v1/embed
        Récupère la liste de tous les embeds actifs.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/embed"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to list embeds"}, 500

    def get_chats_for_embed(self, embed_uuid, token):
        """
        GET /v1/embed/{embedUuid}/chats
        Récupère toutes les conversations pour un embed spécifique.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/embed/{embed_uuid}/chats"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to get chats for embed"}, 500

    def get_chats_for_embed_session(self, embed_uuid, session_uuid, token):
        """
        GET /v1/embed/{embedUuid}/chats/{sessionUuid}
        Récupère les conversations pour un embed et une session spécifiques.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/embed/{embed_uuid}/chats/{session_uuid}"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to get chats for embed session"}, 500
