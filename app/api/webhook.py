from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session
from datetime import date
import httpx
import os
from dotenv import load_dotenv

from app.database import get_session
from app.models import Person
from app.schemas import WebhookResponse

# Load environment variables
load_dotenv()

# Get WayV API credentials from environment
WAYV_TOKEN = os.getenv("WAYV_TOKEN")
TEMPLATE_ID = os.getenv("TEMPLATE_ID")
EXECUTION_COMPANY_ID = os.getenv("EXECUTION_COMPANY_ID")

router = APIRouter(prefix="/api", tags=["webhook"])

@router.post("/webhook", response_model=WebhookResponse)
async def webhook_receive(
    request: Request,
    session: Session = Depends(get_session)
):
    """Receive form submission via webhook, calculate age, and update form"""
    # Parse incoming data
    try:
        data = await request.json()
        
        # Extract person data
        nome_completo = data.get("nome_completo")
        data_nascimento_str = data.get("data_nascimento")
        sexo = data.get("sexo")
        email = data.get("email")
        celular = data.get("celular")
        form_id = data.get("form_id")  # Assuming we get a form ID to update
        
        # Validate required fields
        if not all([nome_completo, data_nascimento_str, sexo, email, form_id]):
            raise HTTPException(status_code=400, detail="Dados incompletos")
            
        # Parse date and calculate age
        data_nascimento = date.fromisoformat(data_nascimento_str)
        hoje = date.today()
        idade = hoje.year - data_nascimento.year - (
            (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
        )
        
        # Save to database
        pessoa = Person(
            nome_completo=nome_completo,
            data_nascimento=data_nascimento,
            sexo=sexo,
            email=email,
            celular=celular,
            idade=idade
        )
        session.add(pessoa)
        session.commit()
        session.refresh(pessoa)
        
        # Check if we have credentials for WayV API
        if not all([WAYV_TOKEN, TEMPLATE_ID, EXECUTION_COMPANY_ID]):
            return WebhookResponse(
                success=True,
                idade_calculada=idade,
                wayv_response=None
            )
        
        # Send age back to update form in WayV
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "Authorization": f"Bearer {WAYV_TOKEN}"
        }
        
        # Prepare payload to update form
        payload = {
            "form_id": form_id,
            "template_id": TEMPLATE_ID,
            "execution_company_id": EXECUTION_COMPANY_ID,
            "fields": {
                "idade": idade
                # Add other required fields according to WayV API documentation
            }
        }
        
        # Send update to WayV
        url = "https://app.way-v.com/api/integration/checklists"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers)
        
        return WebhookResponse(
            success=True,
            idade_calculada=idade,
            wayv_response=response.status_code
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar webhook: {str(e)}")
