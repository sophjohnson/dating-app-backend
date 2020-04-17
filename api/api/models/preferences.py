from sqlalchemy import Column, String, ForeignKey
from .base import Base

class Preferences(Base):

    # Table name
    __tablename__ = 'preferences'

    # Describe columns
    netid = Column(String, primary_key=True, ForeignKey('student.netid'))
    sexualOrientation = Column(String)
    genderIdentity = Column(String)
    mass = Column(String)
    dh = Column(String)
    fridayNights = Column(String)
    password = Column(String)

