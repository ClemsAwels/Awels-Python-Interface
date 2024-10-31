import requests
import os
from dotenv import load_dotenv



class AuthentificationService:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv("BASE_URL")
        print(f"AuthentificationService initialisé sur l'url {self.base_url}")

    def auth(self, **kwargs):
        token = kwargs.get("Authorization")
        if not token:
            return {"error": "No authorization token provided."}, 403

        headers = {"Authorization": token}
        try:
            response = requests.get(self.base_url, headers=headers)
            response.raise_for_status()
            return response.json(), response.status_code
        
        except requests.exceptions.HTTPError as e:
            if response.status_code == 403:
                return {"error": "Invalid API Key"}, 403
            return {"error": "Authentication service error"}, 500
        
        except requests.exceptions.RequestException as e:
            return {"error": "Failed to connect to the authentication service"}, 500
