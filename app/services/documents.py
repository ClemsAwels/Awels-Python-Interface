import requests
import os
from dotenv import load_dotenv
from .authentification import AuthentificationService

class DocumentService:
    def __init__(self, auth_service=None):
        load_dotenv()
        self.auth_service = auth_service or AuthentificationService()
        self.base_url = os.getenv("BASE_URL")
        print("DocumentService initialisé")

    def upload_file(self, file_path, token):
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/document/upload"
        files = {"file": open(file_path, "rb")}
        headers = {"Authorization": token}
        
        try:
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to upload file"}, 500

    def upload_link(self, link, token):
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/document/upload-link"
        json_data = {"link": link}
        headers = {"Authorization": token}
        
        try:
            response = requests.post(url, json=json_data, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to upload link"}, 500

    def upload_raw_text(self, text_content, metadata, token):
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/document/raw-text"
        json_data = {"textContent": text_content, "metadata": metadata}
        headers = {"Authorization": token}

        try:
            response = requests.post(url, json=json_data, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to upload raw text"}, 500

    def list_documents(self, token):
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/documents"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to retrieve document list"}, 500

    def get_accepted_file_types(self, token):
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/document/accepted-file-types"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to retrieve accepted file types"}, 500
