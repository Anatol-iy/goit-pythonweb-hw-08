# Репозиторій (Repository) у FastAPI — це шар, який відповідає за взаємодію з базою даних через 
# SQLAlchemy та абстрагує логіку роботи з базою від бізнес-логіки.

from datetime import timedelta
from typing import List, Optional
from sqlalchemy import func, select, extract  # Додано extract
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased

from src.db.models.contact import Contact
from src.schemas.contact import ContactModel


class ContactRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_contacts(self, skip: int = 0, limit: int = 100, name: Optional[str] = None, surname: Optional[str] = None, email: Optional[str] = None) -> List[Contact]:
        query = select(Contact).offset(skip).limit(limit)
        
        if name:
            query = query.filter(Contact.first_name.ilike(f"%{name}%"))
        if surname:
            query = query.filter(Contact.last_name.ilike(f"%{surname}%"))
        if email:
            query = query.filter(Contact.email.ilike(f"%{email}%"))
        
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_contact(self, contact_id: int) -> Contact | None:
        contact_query = select(Contact).where(Contact.id == contact_id)
        contact = await self.session.execute(contact_query)
        return contact.scalar_one_or_none()

    async def create_contact(self, body: ContactModel) -> Contact:
        new_contact = Contact(
            first_name=body.first_name,
            last_name=body.last_name,
            phone=body.phone,
            email=body.email,
            date_of_birth=body.date_of_birth,
            extra_info=body.extra_info
        )
        
        self.session.add(new_contact)
        await self.session.commit()
        await self.session.refresh(new_contact)  
        return new_contact

    async def update_contact(self, contact_id: int, body: ContactModel) -> Contact | None:
        contact = await self.get_contact(contact_id)
        if contact:
            if body.first_name: contact.first_name = body.first_name
            if body.last_name: contact.last_name = body.last_name
            if body.phone: contact.phone = body.phone
            if body.email: contact.email = body.email
            if body.date_of_birth: contact.date_of_birth = body.date_of_birth
            if body.extra_info: contact.extra_info = body.extra_info

            await self.session.commit()  
            await self.session.refresh(contact)  
            return contact
        return None

    async def delete_contact(self, contact_id: int) -> Contact | None:
        contact = await self.get_contact(contact_id)
        if contact:
            await self.session.delete(contact)  
            await self.session.commit() 
            return contact
        return None

    async def get_birthdays(self, days: int) -> List[Contact]:
        # Пошук контактів, у яких день народження в межах наступних 'days' днів
        query = select(Contact).where(
            extract('month', Contact.date_of_birth) == extract('month', func.current_date()),  # Порівняння місяців
            extract('day', Contact.date_of_birth).between(  # Порівняння днів
                extract('day', func.current_date()),
                extract('day', func.current_date() + timedelta(days=days))
            )
        )
        result = await self.session.execute(query)
        return result.scalars().all()
