# набір маршрутів, контролери - обробляють запити від користувача, викликають відповідні методи з сервісного шару і повертають відповідь
from typing import List, Optional
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Path,
    Query,
    status,
)

from src.services.contacts import ContactService
from src.db.db import get_db
from src.schemas.contact import ContactModel, ContactResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/", response_model=List[ContactResponse])
async def get_contacts(
    db: AsyncSession = Depends(get_db),   #доступ до сесії бази даних
    skip: int = 0,
    limit: int = Query(default=10, le=100, ge=10),
    name: Optional[str] = None,
    surname: Optional[str] = None,
    email: Optional[str] = None,
):
    contact_service = ContactService(db)
    contacts = await contact_service.get_contacts(skip=skip, limit=limit, name=name, surname=surname, email=email)
    return contacts


@router.get("/birthdays", response_model=List[ContactResponse])
async def get_birthdays(
    db: AsyncSession = Depends(get_db),
    days: int = Query(default=7, ge=1, le=30),
):
    contact_service = ContactService(db)
    contacts = await contact_service.get_birthdays(days=days)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(
    contact_id: int = Path(description="Contact ID to fetch", gt=0),
    db: AsyncSession = Depends(get_db),
):
    contact_service = ContactService(db)
    contact = await contact_service.get_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.post("/", response_model=ContactResponse, status_code=status.HTTP_201_CREATED)
async def create_contact(
    body: ContactModel,
    db: AsyncSession = Depends(get_db),
):
    contact_service = ContactService(db)
    return await contact_service.create_contact(body)

# PUT передбачає повну зміну об'єкта
@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactModel,
    contact_id: int = Path(description="Contact ID to be update", gt=0),
    db: AsyncSession = Depends(get_db),
):
    contact_service = ContactService(db)
    contact = await contact_service.update_contact(contact_id, body)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact


@router.delete("/{contact_id}", response_model=ContactResponse)
async def delete_contact(
    contact_id: int = Path(description="Contact ID to be removed", gt=0),
    db: AsyncSession = Depends(get_db),
):
    contact_service = ContactService(db)
    contact = await contact_service.delete_contact(contact_id)
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact
