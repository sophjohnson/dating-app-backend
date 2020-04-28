from sqlalchemy import Column, String, ForeignKey
from .base import Base

class Preferences(Base):

    # Table name
    __tablename__ = 'preferences'

    # Describe columns
    netid               = Column(String, ForeignKey('student.netid'), primary_key=True)
    temperament         = Column(String)
    giveaffection       = Column(String)
    trait               = Column(String)
    idealdate           = Column(String)
    fridaynight         = Column(String)
    dininghall          = Column(String)
    studyspot           = Column(String)
    mass                = Column(String)
    club                = Column(String)
    gameday             = Column(String)
    hour                = Column(String)
    zodiacsign          = Column(String)   
    idealtemperament    = Column(String)
    receiveaffection    = Column(String)
    idealtrait          = Column(String)
