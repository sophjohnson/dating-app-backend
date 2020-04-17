from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base

class Dorm(Base):

    # Table name
    __tablename__ = 'dorm'

    # Describe columns
    dorm = Column(String, primary_key=True)
    mascot = Column(String)
    quad = Column(String)
    logo = Column(String)
    airconditioning = Column(Integer)

    # Initialization
    def __init__(self, dorm, mascot, quad, logo, airconditioning):
        self.dorm = dorm 
        self.mascot = mascot 
        self.quad = quad 
        self.logo = logo 
        self.airconditioning = airconditioning 
