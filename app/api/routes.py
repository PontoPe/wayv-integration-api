from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlmodel import Session, select, delete
from sqlalchemy.sql import func
from typing import List, Optional
from datetime import date

from app.database import get_session
from app.models import Person
from app.schemas import PersonUpdateRequest, SuccessResponse
from app.utils.excel import process_excel_file

router = APIRouter(prefix="/api", tags=["pessoas"])

@router.post("/pessoas/excel", response_model=List[Person])
async def upload_excel(
    file: UploadFile = File(...),
    session: Session = Depends(get_session)
):
    """Upload Excel file and save data to database"""
    # Validate file is Excel
    if not file.filename.endswith(('.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Arquivo deve ser Excel (.xlsx ou .xls)")
    
    try:
        # Read file content
        file_content = await file.read()
        
        # Process Excel file
        pessoas_data = process_excel_file(file_content)
        
        # Insert into database
        pessoas = []
        for data in pessoas_data:
            pessoa = Person(**data)
            session.add(pessoa)
            pessoas.append(pessoa)
            
        session.commit()
        
        # Refresh to get IDs
        for pessoa in pessoas:
            session.refresh(pessoa)
            
        return pessoas
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar arquivo: {str(e)}")

@router.get("/pessoas", response_model=List[Person])
def list_people(
    sexo: Optional[str] = Query(None, description="Filtrar por sexo: Masculino, Feminino ou Outros"),
    session: Session = Depends(get_session)
):
    """List all people, optionally filtered by gender"""
    query = select(Person)
    
    # Apply filter if provided
    if sexo:
        query = query.where(Person.sexo == sexo)
        
    return session.exec(query).all()

@router.put("/pessoas/{id}", response_model=Person)
def update_birthdate(
    id: int, 
    data: PersonUpdateRequest,
    session: Session = Depends(get_session)
):
    """Update a person's birth date"""
    pessoa = session.get(Person, id)
    if not pessoa:
        raise HTTPException(status_code=404, detail="Pessoa não encontrada")
        
    # Update birth date if provided
    if data.data_nascimento:
        pessoa.data_nascimento = data.data_nascimento
        
        # Recalculate age
        hoje = date.today()
        pessoa.idade = hoje.year - pessoa.data_nascimento.year - (
            (hoje.month, hoje.day) < (pessoa.data_nascimento.month, pessoa.data_nascimento.day)
        )
            
    session.add(pessoa)
    session.commit()
    session.refresh(pessoa)
    return pessoa

@router.delete("/pessoas", response_model=SuccessResponse)
def delete_all_records(session: Session = Depends(get_session)):
    """Delete all records from the database"""
    # Count records before deletion
    count_query = select(func.count()).select_from(Person)
    count = session.exec(count_query).one()
    
    # Delete all records
    delete_query = delete(Person)
    session.exec(delete_query)
    session.commit()
    
    return SuccessResponse(
        success=True,
        message=f"{count} registros foram removidos com sucesso"
    )
