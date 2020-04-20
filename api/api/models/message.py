from sqlalchemy import Column, String, Integer, DateTime, Sequence, ForeignKey
from .base import Base

class Message(Base):

    # Table name
    __tablename__ = 'message'

    # Describe columns
    id              = Column(Integer, primary_key=True)
    conversation    = Column(Integer)
    sender          = Column(String, ForeignKey('student.netid'))
    receiver        = Column(String, ForeignKey('student.netid'))
    content         = Column(String)
    timestamp       = Column(DateTime)
