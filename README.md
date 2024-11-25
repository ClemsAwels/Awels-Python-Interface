# Project Name

Description of your project.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/ClemsAwels/Awels-Python-Interface.git
    cd Awels-Python-Interface
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Create a `.env` file in the root directory and add your environment variables:
    ```env
    BASE_URL = your_base_url_here ("http://localhost:8000/api")
    TOKEN= your_token_here
    ```

## Usage

You can modify the main.py script and add new ones (in the app folder), don't forget to import services to use the interface.

### AuthentificationService

To authenticate a user, you can use the `AuthentificationService`:

```python
from services.authentification import AuthentificationService
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
auth_service = AuthentificationService()
response, status_code = auth_service.auth(Authorization=token)
print("Authentication response:", response)
print("Status code:", status_code)
```

### DocumentService

To manage documents, you can use the `DocumentService`:

**Create a User**

```python
from services.admin import AdminService
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
admin_service = AdminService()
response, status_code = admin_service.create_user(username="newuser", password="password", role="default", token=token)
print("Create user response:", response)
print("Status code:", status_code)
```

**List Users**
```python
response, status_code = admin_service.list_users(token=token)
print("List users response:", response)
print("Status code:", status_code)
```

### SystemSettingsService

To manage system settings, you can use the `SystemSettingsService`:

**Dump Settings**

```python
from services.systemsettings import SystemSettingsService
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
system_settings_service = SystemSettingsService()
response, status_code = system_settings_service.dump_settings(token=token)
print("Dump settings response:", response)
print("Status code:", status_code)
```

### DocumentService

To manage documents, you can use the `DocumentService`:

**Upload a File**

```python
from services.documents import DocumentService
import os
from dotenv import load_dotenv

load_dotenv()

token = os.getenv("TOKEN")
document_service = DocumentService()
response, status_code = document_service.upload_file(file_path="path/to/your/file.txt", token=token)
print("Upload file response:", response)
print("Status code:", status_code)
```

## Running Tests

Before running the tests, ensure that multi-user mode is enabled via the UI. The user-related methods are disabled by default and will return errors if not activated.

To run the tests, use the `run_test.py` script. This script will discover and run all test files in the `test` directory that match the pattern `test_*.py`.

1. Ensure you are in the root directory of the project.
2. Run the following command:
    ```sh
    python app/run_test.py
    ```

This will execute all the tests and display the results in the terminal.