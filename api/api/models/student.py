from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from ..models.funFact import FunFact
from ..models.lunch import Lunch

from .base import Base

studentMajor = Table('studentmajor', Base.metadata,
    Column('netid', String, ForeignKey('student.netid'), primary_key=True),
    Column('major', String, ForeignKey('major.major'), primary_key=True)
)

studentMinor = Table('studentminor', Base.metadata,
    Column('netid', String, ForeignKey('student.netid'), primary_key=True),
    Column('minor', String, ForeignKey('minor.minor'), primary_key=True)
)

studentCourse = Table('studentcourse', Base.metadata,
    Column('netid', String, ForeignKey('student.netid'), primary_key=True),
    Column('course', String, ForeignKey('course.id'), primary_key=True)
)

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
    majors          = relationship("Major", secondary=studentMajor)
    minors          = relationship("Minor", secondary=studentMinor)
    courses         = relationship("Course", secondary=studentCourse)
    orientation     = Column(String)
    identity        = Column(String)
    question        = Column(String)
    image           = Column(String)
    funfacts        = relationship("FunFact", backref="student")
    lunches         = relationship("Lunch", back_populates="student")
