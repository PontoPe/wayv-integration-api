from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import date

class Person(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    #optional because it will be auto-incremented, which is also why it has default=None
    nome_completo: str
    data_nascimento: date
    sexo: str
    email: str
    celular: Optional[str] = None
    idade: Optional[int] = None
