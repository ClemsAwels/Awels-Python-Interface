import requests
import os
from dotenv import load_dotenv
from .authentification import AuthentificationService

class OpenAICompatibleService:
    def __init__(self, auth_service=None):
        load_dotenv()
        self.auth_service = auth_service or AuthentificationService()
        self.base_url = os.getenv("BASE_URL")

    def list_models(self, token):
        """
        GET /v1/openai/models
        Récupère tous les modèles disponibles (workspaces pour le chat).
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/openai/models"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500

    def chat_completions(self, model_slug, messages, token, stream=False, temperature=0.7):
        """
        POST /v1/openai/chat/completions
        Exécute une conversation avec un workspace en mode compatibilité OpenAI.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/openai/chat/completions"
        headers = {"Authorization": f"Bearer {token}"}
        json_data = {
            "model": model_slug,
            "messages": messages,
            "stream": stream,
            "temperature": temperature
        }

        try:
            response = requests.post(url, json=json_data, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500

    def get_embeddings(self, input_texts, token, model=None):
        """
        POST /v1/openai/embeddings
        Obtenir les embeddings d'un ou plusieurs textes.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/openai/embeddings"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        payload = {"input": input_texts, "model": model}

        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500
            
    def list_vector_stores(self, token):
        """
        GET /v1/openai/vector_stores
        Liste toutes les collections de bases de données vectorielles connectées.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/openai/vector_stores"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500
