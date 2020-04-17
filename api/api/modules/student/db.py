import binascii
import hashlib
import os
import uuid

from ...models.student import Student
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

        # Hash password
        password = hash_password(body['password'])

        # Create account and profile
        sm = SessionMaker(self.Session)
        with sm as session:
            student = Student(
                netid = body['netid'],
                password = password,
                firstname = body['firstName'],
                lastname = body['lastname'],
                classyear = body['classYear'],
                city = body['city'],
                state = body['state'],
                dorm = body['dorm'],
                sexualorientation = body['sexualOrientation'],
                genderidentity = body['genderIdentity']
            )
            session.add(student)
            session.commit()

            return student.netid

   # Update existing account
    def update_student(self, body):

        # Create account and profile
        sm = SessionMaker(self.Session)
        with sm as session:
            student = Student(
                netid = body['netid'],
                password = password,
                firstname = body['firstName'],
                lastname = body['lastname'],
                classyear = body['classYear'],
                city = body['city'],
                state = body['state'],
                dorm = body['dorm'],
                sexualorientation = body['sexualOrientation'],
                genderidentity = body['genderIdentity']
            )
            session.add(student)
            session.commit()

            return student.netid

    # Get students
    def get_students(self):
        sm = SessionMaker(self.Session)
        with sm as session:
            students = session.query(Student).all()
            students = [{ 'netid' : s.netid,
                          'firstName' : s.firstname,
                          'lastName' : s.lastname } for s in students]
        return students

def hash_password(password):
    salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
    pwdhash = hashlib.pbkdf2_hmac('sha512', password.encode('utf-8'), salt, 100000)
    pwdhash = binascii.hexlify(pwdhash)
    return (salt + pwdhash).decode('ascii')
