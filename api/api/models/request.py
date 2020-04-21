from sqlalchemy import Column, String, DateTime, ForeignKey
from .base import Base

class Request(Base):

    # Table name
    __tablename__ = 'request'

    # Describe columns
    sender          = Column(String, ForeignKey('student.netid'), primary_key=True)
    receiver        = Column(String, ForeignKey('student.netid'), primary_key=True)
    status          = Column(String)
    timestamp       = Column(DateTime)
