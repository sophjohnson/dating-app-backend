from sqlalchemy import Column, String, ForeignKey
from .base import Base

class Browse(Base):

    # Table name
    __tablename__ = 'browse'

    # Describe columns
    viewedFor   = Column(String, ForeignKey('student.netid'), primary_key=True)
    netid       = Column(String, ForeignKey('student.netid'), primary_key=True)
    viewedBy    = Column(String, ForeignKey('student.netid'), primary_key=True)
