from sqlalchemy import Column, String
from .base import Base

class Gender(Base):

    # Table name
    __tablename__ = 'gender'

    # Describe columns
    gender = Column(String, primary_key=True)
