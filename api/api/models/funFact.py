from sqlalchemy import Column, String, Integer, ForeignKey
from .base import Base

class FunFact(Base):

    # Table name
    __tablename__ = 'funfact'

    # Describe columns
    id      = Column(Integer, primary_key=True)
    netid   = Column(String, ForeignKey('student.netid'))
    caption = Column(String)
    photo   = Column(String)
