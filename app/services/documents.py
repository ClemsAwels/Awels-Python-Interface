import requests
import os
from dotenv import load_dotenv
from .authentification import AuthentificationService

class DocumentService:
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

    def upload_file(self, file_path, token):
        """
        POST /v1/document/upload
        Upload un nouveau fichier pour être parsé et préparé pour embedding.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/document/upload"
        files = {'file': open(file_path, 'rb')}

        try:
            return self.handle_request("POST", url, token, files=files)
        except Exception as e:
            return {"error": f"Unexpected error during file upload: {str(e)}"}, 500
        finally:
            files['file'].close()

    def upload_link(self, link, token):
        """
        POST /v1/document/upload-link
        Upload un lien valide pour être scrappé et préparé pour embedding.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/document/upload-link"
        json_data = {"link": link}
        return self.handle_request("POST", url, token, json=json_data)

    def upload_raw_text(self, text_content, metadata, token):
        """
        POST /v1/document/raw-text
        Upload de texte brut avec des métadonnées sans nécessiter de fichier.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/document/raw-text"
        json_data = {
            "textContent": text_content,
            "metadata": metadata
        }
        return self.handle_request("POST", url, token, json=json_data)

    def list_documents(self, token):
        """
        GET /v1/documents
        Obtenir la liste de tous les documents stockés localement.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/documents"
        return self.handle_request("GET", url, token)

    def get_accepted_file_types(self, token):
        """
        GET /v1/document/accepted-file-types
        Obtenir les types de fichiers acceptés pour l'upload.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/document/accepted-file-types"
        return self.handle_request("GET", url, token)

    def get_metadata_schema(self, token):
        """
        GET /v1/document/metadata-schema
        Récupère le schéma des métadonnées pour les uploads de texte brut.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/document/metadata-schema"
        return self.handle_request("GET", url, token)

    def get_document_by_name(self, doc_name, token):
        """
        GET /v1/document/{docName}
        Récupère un document par son nom unique.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/document/{doc_name}"
        return self.handle_request("GET", url, token)

    def create_folder(self, folder_name, token):
        """
        POST /v1/document/create-folder
        Crée un nouveau dossier dans le répertoire de stockage des documents.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/document/create-folder"
        json_data = {"name": folder_name}
        return self.handle_request("POST", url, token, json=json_data)

    def move_files(self, files_to_move, token):
        """
        POST /v1/document/move-files
        Déplace des fichiers dans le répertoire de stockage des documents.
        
        :param files_to_move: Liste de dictionnaires contenant les chemins 'from' et 'to' de chaque fichier.
        """
        auth_response, status_code = self.auth_service.auth(Authorization=token)
        if status_code != 200:
            return {"error": "Authentication failed", "details": auth_response}, status_code

        url = f"{self.base_url}/v1/document/move-files"
        json_data = {"files": files_to_move}
        return self.handle_request("POST", url, token, json=json_data)
