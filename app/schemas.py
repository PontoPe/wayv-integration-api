from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date

# Request model for updating a person
class PersonUpdateRequest(BaseModel):
    data_nascimento: Optional[date] = None
    
# Response model for successful operation
class SuccessResponse(BaseModel):
    success: bool
    message: str
    
# Response model for webhook processing
class WebhookResponse(BaseModel):
    success: bool
    idade_calculada: Optional[int] = None
    wayv_response: Optional[int] = None
