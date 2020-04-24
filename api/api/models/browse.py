from sqlalchemy import Column, String, ForeignKey
from .base import Base

class Browse(Base):

    # Table name
    __tablename__ = 'browse'

    # Describe columns
    viewedfor   = Column(String, ForeignKey('student.netid'), primary_key=True)
    netid       = Column(String, ForeignKey('student.netid'), primary_key=True)
    viewedby    = Column(String, ForeignKey('student.netid'), primary_key=True)
