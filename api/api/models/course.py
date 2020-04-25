from sqlalchemy import Column, String
from .base import Base

class Course(Base):

    # Table name
    __tablename__ = 'course'

    # Describe columns
    id = Column(String, primary_key=True)
    course = Column(String)
