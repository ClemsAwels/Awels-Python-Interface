import importlib

class ServiceManager:
    def __init__(self):
        self.services = {}

    def load_service(self, module_path: str):
        parts = module_path.split('.')
        module_name = parts[0]
        service_class_name = module_name.capitalize() + "Service"

        try:
            module = importlib.import_module(f"app.services.{module_name}")
            service_class = getattr(module, service_class_name)

            service_instance = service_class()
            self.services[module_name] = service_instance
            print(f"{service_class_name} chargé et instancié.")
            return service_instance
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Erreur lors du chargement du service {module_path}: {e}")
            return None

    def execute_service_method(self, module_path: str, method_name: str, kwargs):
        module_name = module_path
        if module_name not in self.services:
            service_instance = self.load_service(module_name)
        else:
            service_instance = self.services[module_name]

        if service_instance:
            method = getattr(service_instance, method_name, None)
            if method:
                try:
                    return method(**kwargs)  # Utilisation de **kwargs ici
                except TypeError as e:
                    print(f"Erreur d'argument pour {method_name}: {e}")
                    return {"error": str(e)}
            else:
                print(f"Le service {module_name} ne possède pas la méthode {method_name}.")
        return None
