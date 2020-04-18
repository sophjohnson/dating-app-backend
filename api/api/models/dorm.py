from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Dorm(Base):

    # Table name
    __tablename__ = 'dorm'

    # Describe columns
    dorm            = Column(String, primary_key=True)
    mascot          = Column(String)
    quad            = Column(String)
    logo            = Column(String)
    airconditioning = Column(Integer)
