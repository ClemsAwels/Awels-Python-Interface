import requests
import os
from dotenv import load_dotenv

class AuthentificationService:
    def __init__(self):
        load_dotenv()
        self.base_url = os.getenv("BASE_URL")
        self.ssl_verify = os.getenv("SSL_VERIFY", "true").lower() == "true"  # Charger SSL_VERIFY depuis les variables d'environnement
        print(f"AuthentificationService initialisé sur l'url {self.base_url} avec SSL_VERIFY={self.ssl_verify}")

    def auth(self, **kwargs):
        token = kwargs.get("Authorization")
        if not token:
            return {"error": "No authorization token provided."}, 403

        url = f"{self.base_url}/v1/auth"
        headers = {"Authorization": token}

        try:
            # Ajouter ssl_verify dans l'appel de la requête
            response = requests.get(url, headers=headers, verify=self.ssl_verify)
            response.raise_for_status()
            return response.json(), response.status_code

        except requests.exceptions.HTTPError as e:
            error_message = f"HTTP Error: {e}"
            try:
                # Inclure le détail de la réponse si disponible
                error_details = response.json()
                error_message = error_details.get("message", str(error_details))
            except ValueError:
                # Si le JSON n'est pas valide, renvoyer le texte brut de la réponse
                error_message = response.text

            if response.status_code == 403:
                return {"error": f"Invalid API Key: {error_message}"}, 403
            return {"error": f"Authentication service error: {error_message}"}, response.status_code

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to connect to the authentication service: {str(e)}"}, 500
