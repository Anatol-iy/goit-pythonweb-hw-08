from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr

# використовується для валідації вхідних даних.
class ContactModel(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr
    date_of_birth: Optional[date] = None
    extra_info: Optional[str] = None 

# для створення(POST) контакта без ID.
class ContactCreate(ContactModel):
    pass 

# використовується для відповіді(GET)  API, додає id
class ContactResponse(ContactModel):
    id: int

# дозволяє Pydantic коректно працювати з об'єктами SQLAlchemy
    model_config = ConfigDict(from_attributes=True)