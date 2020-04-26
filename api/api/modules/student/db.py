import binascii
import hashlib
import os
import uuid

from falcon import HTTPBadRequest

from ...models.student import Student
from ...models.preferences import Preferences
from ...models.dorm import Dorm
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
    def create_student(self, netid, password):

        # Create account and profile
        sm = SessionMaker(self.Session)
        with sm as session:
            student = Student(
                netid           = netid,
                password        = hash_password(password)
            )
            session.add(student)
            session.commit()

            # Add preferences
            preferences = Preferences(
                netid               = netid
            )
            session.add(preferences)
            session.commit()

            return student.netid

   # Update existing student account
    def update_student(self, body, netid):

        # Create account and profile
        sm = SessionMaker(self.Session)
        with sm as session:

            result = session.query(Student, Preferences)\
                            .join(Student.preferences)\
                            .filter(Student.netid == netid).first()

            # If student doesn't exist
            if result is None:
                msg = "No student exists for given netid."
                raise HTTPBadRequest("Bad Request", msg)

            (student, pref) = result

            if 'majors' in body:
                student.majors.clear()
                session.commit()
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
            student.question        = body.get('question', student.question)

            session.commit()

            pref.temperament         = body.get('temperament', pref.temperament)
            pref.giveaffection       = body.get('giveAffection', pref.giveaffection)
            pref.trait               = body.get('trait', pref.trait)
            pref.idealdate           = body.get('idealDate', pref.idealdate)
            pref.fridaynight         = body.get('fridayNight', pref.fridaynight)
            pref.dininghall          = body.get('diningHall', pref.dininghall)
            pref.studyspot           = body.get('studySpot', pref.studyspot)
            pref.mass                = body.get('mass', pref.mass)
            pref.club                = body.get('club', pref.club)
            pref.gameday             = body.get('gameDay', pref.gameday)
            pref.hour                = body.get('hour', pref.hour)
            pref.idealtemperament    = body.get('idealTemperament', pref.idealtemperament)
            pref.receiveaffection    = body.get('receiveAffection', pref.receiveaffection)
            pref.idealtrait          = body.get('idealTrait', pref.idealtrait)

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
                                     .join(Student.preferences)\
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
                        'question'          : student.question,
                        'image'             : student.image,
                        'temperament'       : pref.temperament,
                        'giveAffection'     : pref.giveaffection,
                        'trait'             : pref.trait,
                        'idealDate'         : pref.idealdate,
                        'fridayNight'       : pref.fridaynight,
                        'diningHall'        : pref.dininghall,
                        'studySpot'         : pref.studyspot,
                        'mass'              : pref.mass,
                        'club'              : pref.club,
                        'gameDay'           : pref.gameday,
                        'hour'              : pref.hour,
                        'idealTemperament'  : pref.idealtemperament,
                        'receiveAffection'  : pref.receiveaffection,
                        'idealTrait'        : pref.idealtrait }

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
                        'question'          : student.question,
                        'image'             : student.image,
                        'funFacts'          : [ self.format_fun_fact(f) for f in student.funfacts ] }

        return student

    def format_fun_fact(self, funFact):
        funFact = { 'id'      : funFact.id,
                    'netid'   : funFact.netid,
                    'caption' : funFact.caption,
                    'image'   : funFact.image }

        return funFact

    # Get dorm object
    def unpack_dorm(self, dorm):
        sm = SessionMaker(self.Session)
        with sm as session:
            dorm = session.query(Dorm.dorm).filter(Dorm.dorm == dorm).scalar()
            return dorm

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
