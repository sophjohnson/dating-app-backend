from sqlalchemy import Column, String
from .base import Base

class Major(Base):

    # Table name
    __tablename__ = 'major'

    # Describe columns
    major = Column(String, primary_key=True)
