import requests
import os
from dotenv import load_dotenv
from .authentification import AuthentificationService

class WorkspaceService:
    def __init__(self, auth_service=None):
        load_dotenv()
        self.auth_service = auth_service or AuthentificationService()
        self.base_url = os.getenv("BASE_URL")

    def create_workspace(self, name, token):
        """
        POST /v1/workspace/new
        Create a new workspace with the specified name.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/workspace/new"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        data = {"name": name}

        try:
            response = requests.post(url, headers=headers, json=data)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500

    def list_workspaces(self, token):
        """
        GET /v1/workspaces
        List all current workspaces.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/workspaces"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500

    def get_workspace_by_slug(self, slug, token):
        """
        GET /v1/workspace/{slug}
        Retrieve a workspace by its unique slug.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/workspace/{slug}"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500

    def delete_workspace(self, slug, token):
        """
        DELETE /v1/workspace/{slug}
        Delete a workspace by its unique slug.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/workspace/{slug}"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.delete(url, headers=headers)
            response.raise_for_status()
            return {"message": "Workspace deleted successfully"}, response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500

    def update_workspace(self, slug, update_data, token):
        """
        POST /v1/workspace/{slug}/update
        Update a workspace's settings by its unique slug.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/workspace/{slug}/update"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        try:
            response = requests.post(url, headers=headers, json=update_data)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500

    def get_workspace_chats(self, slug, token):
        """
        GET /v1/workspace/{slug}/chats
        Retrieve chats associated with a specific workspace slug.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/workspace/{slug}/chats"
        headers = {"Authorization": f"Bearer {token}"}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500

    def update_workspace_embeddings(self, slug, embeddings_data, token):
        """
        POST /v1/workspace/{slug}/update-embeddings
        Update embeddings by adding or removing documents for a workspace.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/workspace/{slug}/update-embeddings"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        try:
            response = requests.post(url, headers=headers, json=embeddings_data)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500

    def update_workspace_pin(self, slug, pin_data, token):
        """
        POST /v1/workspace/{slug}/update-pin
        Update pin status for a document in the workspace.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/workspace/{slug}/update-pin"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        try:
            response = requests.post(url, headers=headers, json=pin_data)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500

    def chat_with_workspace(self, slug, chat_data, token):
        """
        POST /v1/workspace/{slug}/chat
        Execute a chat with the specified workspace.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/workspace/{slug}/chat"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        try:
            response = requests.post(url, headers=headers, json=chat_data)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500

    def stream_chat_with_workspace(self, slug, chat_data, token):
        """
        POST /v1/workspace/{slug}/stream-chat
        Execute a streamable chat with the specified workspace.
        """
        auth_response, status_code = self.auth_service.auth(token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/workspace/{slug}/stream-chat"
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

        try:
            response = requests.post(url, headers=headers, json=chat_data, stream=True)
            response.raise_for_status()
            return response.iter_lines(), response.status_code
        except requests.exceptions.HTTPError as http_err:
            return {"error": "HTTP error occurred", "details": str(http_err)}, response.status_code
        except requests.exceptions.RequestException as req_err:
            return {"error": "Request exception occurred", "details": str(req_err)}, 500
