from sqlalchemy import Column, String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .base import Base

class Lunch(Base):

    # Table name
    __tablename__ = 'lunch'

    # Describe columns
    id          = Column(Integer, primary_key=True)
    netid       = Column(String, ForeignKey('student.netid'))
    day         = Column(String)
    starttime   = Column(DateTime)
    endtime     = Column(DateTime)
    student     = relationship("Student", back_populates="lunches")
