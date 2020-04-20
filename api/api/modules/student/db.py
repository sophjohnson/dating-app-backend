import binascii
import hashlib
import os
import uuid

from ...models.student import Student
from ...models.major import Major
from ...models.minor import Minor
from ...utils import SessionMaker

class db:

    def __init__(self, Session):
        self.Session = Session

    # Check if netid is taken
    def student_exists(self, id):
        sm = SessionMaker(self.Session)
        with sm as session:
            student = session.query(Student.netid).filter_by(netid=id).scalar()

        return student is not None

   # Create new account
    def create_student(self, body):

        # Create account and profile
        sm = SessionMaker(self.Session)
        with sm as session:
            student = Student(
                netid           = body['netid'],
                password        = hash_password(body['password']),
                firstname       = body['firstName'],
                lastname        = body['lastName'],
                gradyear        = body['gradYear'],
                city            = body['city'],
                state           = body['state'],
                dorm            = body['dorm'],
                majors          = self.unpack_majors(body['majors']),
                minors          = self.unpack_minors(body['minors']),
                orientation     = body['sexualOrientation'],
                identity        = body['genderIdentity']
            )
            session.add(student)
            session.commit()

            return student.netid

   # Update existing account
    def update_student(self, body):

        # Create account and profile
        sm = SessionMaker(self.Session)
        with sm as session:

            student = session.query(Student).filter(Student.netid == body["netid"]).first()

            # If update password
            if 'password' in body:
                password = hash_password(body['password']),

            if 'majors' in body:
                student.majors = self.unpack_majors(body['majors'])

            if 'minors' in body:
                student.minors = self.unpack_minors(body['minors'])

            # Handle other updates
            student.firstname       = body.get('firstName', student.firstname)
            student.lastname        = body.get('lastName', student.lastname)
            student.gradyear        = body.get('gradYear', student.gradyear)
            student.city            = body.get('city', student.city)
            student.state           = body.get('state', student.state)
            student.dorm            = body.get('dorm', student.dorm)
            student.orientation     = body.get('sexualOrientation', student.orientation)
            student.identity        = body.get('genderIdentity', student.identity)

            session.commit()

            return student.netid

    # Get students
    def get_students(self):
        sm = SessionMaker(self.Session)
        with sm as session:
            students = session.query(Student).all()
            students = [{ 'netid'       : s.netid,
                          'funFacts'    : [ self.format_fun_fact(f) for f in s.funfacts ],
                          'minors'      : [ m.minor for m in s.minors ],
                          'lastName'    : s.lastname    } for s in students]
        return students

    def format_fun_fact(self, funFact):
        funFact = { 'id'      : funFact.id,
                    'netid'   : funFact.netid,
                    'caption' : funFact.caption,
                    'photo'   : funFact.photo }

        return funFact

    # Get major objects
    def unpack_majors(self, majors):
        sm = SessionMaker(self.Session)
        with sm as session:
            return [ session.query(Major).filter(Major.major == m).first() for m in majors ]

    # Get minor objects
    def unpack_minors(self, minors):
        sm = SessionMaker(self.Session)
        with sm as session:
            minors = [ session.query(Minor).filter(Minor.minor == m).first() for m in minors ]
            return [ m for m in minors if m is not None]

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
