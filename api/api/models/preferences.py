from sqlalchemy import Column, String, ForeignKey
from .base import Base

class Preferences(Base):

    # Table name
    __tablename__ = 'preferences'

    # Describe columns
    netid           = Column(String, ForeignKey('student.netid'), primary_key=True)
    mass            = Column(String)
    dh              = Column(String)
    friday    = Column(String)
