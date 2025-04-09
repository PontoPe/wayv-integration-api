import pandas as pd
from app.models import Person
from datetime import date
from typing import List

def process_excel_file(file_content: bytes) -> List[dict]:
    """Process an Excel file and extract person data"""
    df = pd.read_excel(file_content)
    
    # Validate required columns
    required_columns = ["Nome Completo", "Data de Nascimento", "Sexo", "E-mail"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError("Arquivo Excel não contém todas as colunas necessárias")
    
    # Convert DataFrame to list of dictionaries
    pessoas = []
    for _, row in df.iterrows():
        # Handle data types and format date
        if isinstance(row["Data de Nascimento"], str):
            data_nascimento = date.fromisoformat(row["Data de Nascimento"])
        else:
            data_nascimento = row["Data de Nascimento"]
            
        pessoa = {
            "nome_completo": row["Nome Completo"],
            "data_nascimento": data_nascimento,
            "sexo": row["Sexo"],
            "email": row["E-mail"],
            "celular": row.get("Celular", None)
        }
        pessoas.append(pessoa)
    
    return pessoas
