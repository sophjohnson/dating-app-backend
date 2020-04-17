from sqlalchemy import Column, String
#from sqlalchemy.ext.declarative import declarative_base
from .base import Base

#Base = declarative_base()

class State(Base):

    # Table name
    __tablename__ = 'state'

    # Describe columns
    state = Column(String, primary_key=True)
    code = Column(String)

    # Initialization
    def __init__(self, code, state):
        self.code = code
        self.state = state 
