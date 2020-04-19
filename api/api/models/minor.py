from sqlalchemy import Column, String
from .base import Base

class Minor(Base):

    # Table name
    __tablename__ = 'minor'

    # Describe columns
    minor = Column(String, primary_key=True)
