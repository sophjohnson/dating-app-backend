from sqlalchemy import Column, String, DateTime, ForeignKey
from .base import Base

class Recommendation(Base):

    # Table name
    __tablename__ = 'recommendation'

    # Describe columns
    viewer          = Column(String, ForeignKey('student.netid'), primary_key=True)
    viewee          = Column(String, ForeignKey('student.netid'), primary_key=True)
    status          = Column(String)
    recommendedby   = Column(String)
    timestamp       = Column(DateTime)
