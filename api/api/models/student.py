from sqlalchemy import Column, String, ForeignKey
from .base import Base

class Student(Base):

    # Table name
    __tablename__ = 'student'

    # Describe columns
    netid           = Column(String, primary_key=True)
    password        = Column(String)
    firstname       = Column(String)
    lastname        = Column(String)
    gradyear        = Column(String)
    city            = Column(String)
    state           = Column(String, ForeignKey('state.state'))
    dorm            = Column(String, ForeignKey('dorm.dorm'))
    orientation     = Column(String)
    identity        = Column(String)
