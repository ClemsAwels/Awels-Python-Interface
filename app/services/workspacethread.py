import requests
import os
from dotenv import load_dotenv
from .authentification import AuthentificationService

class WorkspaceThreadService:
    def __init__(self, auth_service=None):
        load_dotenv()
        self.auth_service = auth_service or AuthentificationService()
        self.base_url = os.getenv("BASE_URL")

    def create_thread(self, slug, user_id, token):
        """
        POST /v1/workspace/{slug}/thread/new
        Crée un nouveau thread dans l'espace de travail.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/workspace/{slug}/thread/new"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        data = {"userId": user_id} if user_id else {}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to create thread"}, 500

    def update_thread(self, slug, thread_slug, new_name, token):
        """
        POST /v1/workspace/{slug}/thread/{threadSlug}/update
        Met à jour le nom d'un thread dans un espace de travail.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/workspace/{slug}/thread/{thread_slug}/update"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        data = {"name": new_name}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to update thread name"}, 500

    def delete_thread(self, slug, thread_slug, token):
        """
        DELETE /v1/workspace/{slug}/thread/{threadSlug}
        Supprime un thread d'un espace de travail.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/workspace/{slug}/thread/{thread_slug}"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to delete thread"}, 500

    def get_thread_chats(self, slug, thread_slug, token):
        """
        GET /v1/workspace/{slug}/thread/{threadSlug}/chats
        Récupère les chats d'un thread dans un espace de travail.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/workspace/{slug}/thread/{thread_slug}/chats"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to get thread chats"}, 500

    def chat_with_thread(self, slug, thread_slug, message, mode, user_id, token):
        """
        POST /v1/workspace/{slug}/thread/{threadSlug}/chat
        Envoie un message pour converser avec un thread dans un espace de travail.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/workspace/{slug}/thread/{thread_slug}/chat"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        data = {
            "message": message,
            "mode": mode,
            "userId": user_id
        }

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to chat with thread"}, 500

    def stream_chat_with_thread(self, slug, thread_slug, message, mode, user_id, token):
        """
        POST /v1/workspace/{slug}/thread/{threadSlug}/stream-chat
        Envoie un message en mode chat en continu avec un thread dans un espace de travail.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/workspace/{slug}/thread/{thread_slug}/stream-chat"
        headers = {
            "Authorization": token,
            "Content-Type": "application/json"
        }
        data = {
            "message": message,
            "mode": mode,
            "userId": user_id
        }

        try:
            response = requests.post(url, headers=headers, json=data, stream=True)
            response.raise_for_status()
            return response.iter_lines(decode_unicode=True), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to stream chat with thread"}, 500
