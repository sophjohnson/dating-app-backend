from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
#from .state import State
from .base import Base

#Base = declarative_base()

class Student(Base):

    # Table name
    __tablename__ = 'student'

    # Describe columns
    netid = Column(String, primary_key=True)
    firstname = Column(String)
    lastname = Column(String)
    classyear = Column(String)
    city = Column(String)
    state = Column(String, ForeignKey('state.state'))
    password = Column(String)

