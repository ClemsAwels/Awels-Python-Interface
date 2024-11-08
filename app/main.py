from services import *
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")


# Test AuthentificationService
auth_service = AuthentificationService()
response, status_code = auth_service.auth(token)
print("Réponse de l'authentification :", response)
print("Code de statut :", status_code)

# Test AdminService
admin_service = AdminService()
admin_response = admin_service.create_user(username="test", password="test", role="user", token=token)
print("Réponse du service admin :", admin_response)
admin_response  = admin_service.list_users(token=token)
print("Réponse du service admin :", admin_response)


# Test SystemSettingsService
system_settings_service = SystemSettingsService()
settings_response = system_settings_service.get_system_settings(token=token)
print("Réponse du service system settings :", settings_response)

