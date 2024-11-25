from services import *
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")


# Test AuthentificationService
auth_service = AuthentificationService()
response, status_code = auth_service.auth(Authorization=token)
print("Réponse de l'authentification :", response)
print("Code de statut :", status_code)

# Test AdminService
admin_service = AdminService()
admin_response = admin_service.create_user(username="test", password="testtest", role="default", token=token)
print("Réponse du service admin :", admin_response)
admin_response  = admin_service.list_users(token=token)
print("Réponse du service admin :", admin_response)


# Test SystemSettingsService
system_settings_service = SystemSettingsService()
settings_response = system_settings_service.get_system_settings(token=token)
print("Réponse du service system settings :", settings_response)

# Test UserService
# Définissez les informations de l'utilisateur à mettre à jour
user_id = "2"
username = "nouveau_nom_utilisateur"
password = "nouveau_mot_de_passe"
role = "default"
suspended = False

# Appelez la méthode update_user
response, status_code = admin_service.update_user(
    user_id=user_id,
    username=username,
    password=password,
    role=role,
    suspended=suspended,
    token=token
)

# Affichez la réponse
print(response, status_code)

