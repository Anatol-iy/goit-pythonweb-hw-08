# створення моделі
from sqlalchemy import Integer, String, Date, Column
from src.db.models.base import Base


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    extra_info = Column(String, nullable=True) 