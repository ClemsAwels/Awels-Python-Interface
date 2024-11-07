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
        """
        POST /v1/document/upload
        Upload un nouveau fichier pour être parsé et préparé pour embedding.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/document/upload"
        headers = {"Authorization": token}
        files = {'file': open(file_path, 'rb')}
        
        try:
            response = requests.post(url, files=files, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to upload file"}, 500

    def upload_link(self, link, token):
        """
        POST /v1/document/upload-link
        Upload un lien valide pour être scrappé et préparé pour embedding.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/document/upload-link"
        headers = {"Authorization": token}
        json_data = {"link": link}

        try:
            response = requests.post(url, json=json_data, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to upload link"}, 500

    def upload_raw_text(self, text_content, metadata, token):
        """
        POST /v1/document/raw-text
        Upload de texte brut avec des métadonnées sans nécessiter de fichier.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/document/raw-text"
        headers = {"Authorization": token}
        json_data = {
            "textContent": text_content,
            "metadata": metadata
        }

        try:
            response = requests.post(url, json=json_data, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to upload raw text"}, 500

    def list_documents(self, token):
        """
        GET /v1/documents
        Obtenir la liste de tous les documents stockés localement.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/documents"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to list documents"}, 500

    def get_accepted_file_types(self, token):
        """
        GET /v1/document/accepted-file-types
        Obtenir les types de fichiers acceptés pour l'upload.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/document/accepted-file-types"
        headers = {"Authorization": token}

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to get accepted file types"}, 500

    def get_metadata_schema(self, token):
        """
        GET /v1/document/metadata-schema
        Récupère le schéma des métadonnées pour les uploads de texte brut.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/document/metadata-schema"
        headers = {"Authorization": token}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to retrieve metadata schema"}, 500

    def get_document_by_name(self, doc_name, token):
        """
        GET /v1/document/{docName}
        Récupère un document par son nom unique.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/document/{doc_name}"
        headers = {"Authorization": token}
        
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to retrieve document"}, 500

    def create_folder(self, folder_name, token):
        """
        POST /v1/document/create-folder
        Crée un nouveau dossier dans le répertoire de stockage des documents.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/document/create-folder"
        headers = {"Authorization": token}
        json_data = {"name": folder_name}

        try:
            response = requests.post(url, json=json_data, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to create folder"}, 500

    def move_files(self, files_to_move, token):
        """
        POST /v1/document/move-files
        Déplace des fichiers dans le répertoire de stockage des documents.
        
        :param files_to_move: Liste de dictionnaires contenant les chemins 'from' et 'to' de chaque fichier.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return auth_response, status_code

        url = f"{self.base_url}/v1/document/move-files"
        headers = {"Authorization": token}
        json_data = {"files": files_to_move}

        try:
            response = requests.post(url, json=json_data, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.RequestException:
            return {"error": "Failed to move files"}, 500