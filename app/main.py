from flask import current_app as app, request, jsonify
from .services.service_manager import ServiceManager

# Initialisation de ServiceManager
manager = ServiceManager()

@app.route('/execute', methods=['POST'])
def execute():
    # Récupération des données JSON envoyées avec la requête POST
    data = request.json
    if not data or 'method' not in data:
        return jsonify({"error": "Le champ 'method' est requis"}), 400

    # Extraction du nom de service et de la méthode depuis "method"
    full_method = data['method']
    parts = full_method.split('.')
    if len(parts) != 2:
        return jsonify({"error": "Le format du champ 'method' doit être 'service.method'"}), 400

    service = parts[0]      # Exemple : 'documents'
    method = parts[1]       # Exemple : 'upload'
    kwargs = {k: v for k, v in data.items() if k not in ['method']}

    # Exécution de la méthode du service
    result = manager.execute_service_method(service, method, kwargs)

    if result is None:
        return jsonify({"error": "Le service ou la méthode spécifiée est introuvable"}), 404

    # Retourne le résultat sous forme de JSON
    return jsonify({"result": result})
