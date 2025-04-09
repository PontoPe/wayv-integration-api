# WayV Integration API

API para gerenciar e integrar dados de formulários com a plataforma WayV.

## Funcionalidades

- Inserção de dados via arquivo Excel
- Listagem e filtro de registros
- Atualização de datas de nascimento
- Recebimento de dados via webhook e cálculo de idade
- Limpeza de registros

## Requisitos

- Python 3.9+
- Dependências listadas em `requirements.txt`

## Instalação

### 1. Clone o repositório:

"git clone https://github.com/pontope/wayv-integration-api.git"

### 2. Navegue até o diretório do projeto:
"cd wayv-integration-api"

### 3. Crie um ambiente virtual (opcional, mas recomendado):
"python -m venv venv"
"source venv/bin/activate" (Linux/Mac)
"venv\Scripts\activate" (Windows)

### 4. Instale as dependências:
"pip install -r requirements.txt"

### 5. Configure as variáveis de ambiente necessárias:
Popule as variáveis de ambiente no arquivo `.env` com os valores apropriados.



## Executando a API
uvicorn app.main --reload

A API estará disponível em http://localhost:8000 e a documentação em http://localhost:8000/docs
Endpoints


### 1. Inserção de Dados
POST /api/pessoas/excel

Aceita um arquivo Excel (.xlsx ou .xls)
Retorna a lista de pessoas inseridas

Exemplo de chamada:
curl -X POST "http://localhost:8000/api/pessoas/excel" 
-H "accept: application/json" 
-H "Content-Type: multipart/form-data" 
-F "file=@dados.xlsx"


### 2. Listagem de Dados
GET /api/pessoas

Lista todos os registros
Opção de filtrar por sexo

Exemplo de chamada:
curl -X GET "http://localhost:8000/api/pessoas?sexo=Masculino" 
-H "accept: application/json"


### 3. Atualização de Dados
PUT /api/pessoas/{id}

Atualiza a data de nascimento de um registro

Exemplo de chamada:
curl -X PUT "http://localhost:8000/api/pessoas/1" 
-H "accept: application/json" 
-H "Content-Type: application/json" 
-d '{"data_nascimento": "1990-01-15"}'


### 4. Webhook
POST /api/webhook

Recebe dados do formulário
Calcula idade
Atualiza o formulário correspondente

Exemplo de chamada:
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


### 5. Limpeza de Dados
DELETE /api/pessoas

Remove todos os registros da base de dados

Exemplo de chamada:
curl -X DELETE "http://localhost:8000/api/pessoas" 
-H "accept: application/json"

## Integração com WayV
A integração com a plataforma WayV é feita através do endpoint de webhook, que calcula a idade com base na data de nascimento e envia essa informação de volta para o formulário correspondente.

