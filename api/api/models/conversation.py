from sqlalchemy import Column, String, Integer, ForeignKey
from .base import Base

class Conversation(Base):

    # Table name
    __tablename__ = 'conversation'

    # Describe columns
    id          = Column(Integer, primary_key=True)
    student1    = Column(String, ForeignKey('student.netid'))
    student2    = Column(String, ForeignKey('student.netid'))
