[![pt-br](https://img.shields.io/badge/lang-pt--br-green.svg)](https://github.com/PontoPe/wayv-integration-api/blob/master/README-ptbr.md)

# WayV Integration API
API to manage and integrate form data with the WayV platform.

## Features:

### Data insertion via Excel files
Listing and filtering of records
Birth date updates
Receiving data via webhook and age calculation
Database cleanup


## Requirements

Python 3.9+
Dependencies listed in requirements.txt


## Installation

### 1. Clone the repository:
"git clone https://github.com/pontope/wayv-integration-api.git"

### 2. Navigate to the project directory:
"cd wayv-integration-api"

### 3. Create a virtual environment (optional, but recommended):
"python -m venv venv"
"source venv/bin/activate" (Linux/Mac)
"venv\Scripts\activate" (Windows)

### 4. Install the dependencies:
"pip install -r requirements.txt"

### 5. Configure the necessary environment variables:
Populate the environment variables in the .env file with the appropriate values.
Running the API
uvicorn app.main --reload
The API will be available at http://localhost:8000 and the documentation at http://localhost:8000/docs


## Endpoints

### 1. Data Insertion
POST /api/pessoas/excel
Accepts an Excel file (.xlsx or .xls)
Returns the list of inserted people
Example call:
curl -X POST "http://localhost:8000/api/pessoas/excel"
-H "accept: application/json"
-H "Content-Type: multipart/form-data"
-F "file=@dados.xlsx"

### 2. Data Listing
GET /api/pessoas
Lists all records
Option to filter by gender
Example call:
curl -X GET "http://localhost:8000/api/pessoas?sexo=Masculino"
-H "accept: application/json"

### 3. Data Update
PUT /api/pessoas/{id}
Updates a record's birth date
Example call:
curl -X PUT "http://localhost:8000/api/pessoas/1"
-H "accept: application/json"
-H "Content-Type: application/json"
-d '{"data_nascimento": "1990-01-15"}'

### 4. Webhook
POST /api/webhook
Receives form data
Calculates age
Updates the corresponding form
Example call:
curl -X POST "http://localhost:8000/api/webhook"
-H "accept: application/json"
-H "Content-Type: application/json"
-d '{
"nome_completo": "João Silva",
"data_nascimento": "1990-05-15",
"sexo": "Masculino",
"email": "joao@example.com",
"celular": "11987654321",
"form_id": "12345"
}'

### 5. Data Cleanup
DELETE /api/pessoas
Removes all records from the database
Example call:
curl -X DELETE "http://localhost:8000/api/pessoas"
-H "accept: application/json"


## WayV Integration
Integration with the WayV platform is done through the webhook endpoint, which calculates age based on birth date and sends this information back to the corresponding form.
