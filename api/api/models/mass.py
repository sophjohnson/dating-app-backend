from sqlalchemy import Column, String, ForeignKey
from .base import Base

class Mass(Base):

    # Table name
    __tablename__ = 'mass'

    # Describe columns
    massid      = Column(String, primary_key=True)
    location    = Column(String)
    day         = Column(String)
    time        = Column(String)
