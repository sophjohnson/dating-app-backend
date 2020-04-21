import binascii
import hashlib
import os
import uuid

from falcon import HTTPBadRequest

from ...models.student import Student
from ...models.preferences import Preferences
from ...models.major import Major
from ...models.minor import Minor
from ...utils import SessionMaker
from ..image.resource import ImageHandler


class db:

    def __init__(self, Session):
        self.Session = Session
        self.ImageHandler = ImageHandler(os.path.dirname(__file__))

    # Check if netid is taken
    def student_exists(self, id):
        sm = SessionMaker(self.Session)
        with sm as session:
            student = session.query(Student.netid).filter(Student.netid == id).scalar()

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

            # Add preferences
            preferences = Preferences(
                netid   = body['netid'],
                dh      = body['dh'],
                friday  = body['fridayNights'],
                mass    = body['attendsMass']
            )
            session.add(preferences)
            session.commit()

            return student.netid

   # Update existing student account
    def update_student(self, body, netid):

        # Create account and profile
        sm = SessionMaker(self.Session)
        with sm as session:

            student = session.query(Student).filter(Student.netid == netid).first()

            # If student doesn't exist
            if student is None:
                msg = "No student exists for given netid."
                raise HTTPBadRequest("Bad Request", msg)

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

    def update_image(self, req, netid):

        # Update image path if successful
        sm = SessionMaker(self.Session)
        with sm as session:
            student = session.query(Student).filter(Student.netid == netid).scalar()

            # If student doesn't exist
            if student is None:
                msg = "No student exists for given netid."
                raise HTTPBadRequest("Bad Request", msg)

            # Delete current profile picture
            if student.image is not None:
                self.ImageHandler.delete_image(student.image)

            # Save image and record path
            student.image = self.ImageHandler.save_image(req, netid, 0)

            session.commit()

            return student.netid

    # Get all information about student
    def get_student(self, netid):
        sm = SessionMaker(self.Session)
        with sm as session:

            result = session.query(Student, Preferences)\
                                     .join(Preferences, Student.netid == Preferences.netid)\
                                     .filter(Student.netid == netid).first()

            # If student doesn't exist
            if result is None:
                msg = "No student exists for given netid."
                raise HTTPBadRequest("Bad Request", msg)

            (student, pref) = result

            student = { 'netid'             : student.netid,
                        'firstName'         : student.firstname,
                        'lastName'          : student.lastname,
                        'gradYear'          : student.gradyear,
                        'majors'            : [ m.major for m in student.majors ],
                        'minors'            : [ m.minor for m in student.minors ],
                        'city'              : student.city,
                        'state'             : student.state,
                        'dorm'              : student.dorm,
                        'sexualOrientation' : student.orientation,
                        'genderIdentity'    : student.identity,
                        'funFacts'          : [ self.format_fun_fact(f) for f in student.funfacts ],
                        'image'             : student.image,
                        'dh'                : pref.dh,
                        'fridayNights'      : pref.friday,
                        'attendsMass'       : pref.mass }

        return student

    # Get only profile information for viewing
    def get_profile(self, netid):
        sm = SessionMaker(self.Session)
        with sm as session:

            student = session.query(Student).filter(Student.netid == netid).first()

            student = { 'netid'             : student.netid,
                        'firstName'         : student.firstname,
                        'lastName'          : student.lastname,
                        'gradYear'          : student.gradyear,
                        'majors'            : [ m.major for m in student.majors ],
                        'minors'            : [ m.minor for m in student.minors ],
                        'city'              : student.city,
                        'state'             : student.state,
                        'dorm'              : student.dorm,
                        'funFacts'          : [ self.format_fun_fact(f) for f in student.funfacts ] }

        return student

    def format_fun_fact(self, funFact):
        funFact = { 'id'      : funFact.id,
                    'netid'   : funFact.netid,
                    'caption' : funFact.caption,
                    'image'   : funFact.image }

        return funFact

    # Get major objects
    def unpack_majors(self, majors):
        sm = SessionMaker(self.Session)
        with sm as session:
            majors = [ session.query(Major).filter(Major.major == m).first() for m in majors ]
            return [ m for m in majors if m is not None]

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
