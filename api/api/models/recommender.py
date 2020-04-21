from sqlalchemy import Column, String, ForeignKey
from .base import Base

class Recommender(Base):

    # Table name
    __tablename__ = 'recommender'

    # Describe columns
    recommender = Column(String, ForeignKey('student.netid'), primary_key=True)
    recommendee = Column(String, ForeignKey('student.netid'), primary_key=True)
