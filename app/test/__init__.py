import os
from dotenv import load_dotenv

# Charger les variables d'environnement à partir d'un fichier .env
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

# (Optionnel) Ajouter le dossier `app` au chemin Python si nécessaire
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))