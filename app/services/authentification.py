import requests

class AuthentificationService:
    def __init__(self):
        print("AuthentificationService initialisé")

    def auth(self, **kwargs):
        # URL de l'endpoint d'authentification externe
        auth_url = "http://localhost:8000/api/v1/auth"

        # Récupérer le token depuis les kwargs (transmis par le ServiceManager)
        token = kwargs.get("Authorization")
        if not token:
            return {"error": "No authorization token provided."}, 403

        # Effectuer une requête POST vers l'API d'authentification externe
        headers = {"Authorization": token}
        try:
            response = requests.get(auth_url, headers=headers)
            response.raise_for_status()  # Lève une exception si le code de statut est 4xx ou 5xx

            # Retourne le JSON de la réponse en cas de succès
            return response.json(), response.status_code
        except requests.exceptions.HTTPError as e:
            # Gère les erreurs HTTP et retourne un message d'erreur approprié
            if response.status_code == 403:
                return {"error": "Invalid API Key"}, 403
            return {"error": "Authentication service error"}, 500
        except requests.exceptions.RequestException as e:
            # Gère d'autres erreurs de connexion
            return {"error": "Failed to connect to the authentication service"}, 500
