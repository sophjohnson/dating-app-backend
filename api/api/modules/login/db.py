import binascii
import hashlib
import os
import uuid

from falcon import HTTPBadRequest,HTTPUnauthorized

from ...models.student import Student
from ...utils import SessionMaker
from ..student.db import hash_password

class db:

    def __init__(self, Session):
        self.Session = Session

    # Validate password for netid account
    def validate(self, netid, password):

        sm = SessionMaker(self.Session)
        with sm as session:
            student = session.query(Student).filter(Student.netid == netid).first()
            if student is None:
                msg = "Given netid is not in the system."
                raise HTTPUnauthorized("Student netid not found", msg)

            if not verify_password(student.password, password):
                msg = "Wrong password for given netid."
                raise HTTPUnauthorized("Incorrect password", msg)

            return True

    # Update student's password
    def update_password(self, netid, password):

        sm = SessionMaker(self.Session)
        with sm as session:
            student = session.query(Student).filter(Student.netid == netid).scalar()
            student.password = hash_password(password)
            session.commit()

# Verify a stored password against one provided by user
def verify_password(storedPassword, providedPassword):
    salt = storedPassword[:64]
    storedPassword = storedPassword[64:]
    pwdhash = hashlib.pbkdf2_hmac('sha512',
                                  providedPassword.encode('utf-8'),
                                  salt.encode('ascii'),
                                  100000)
    pwdhash = binascii.hexlify(pwdhash).decode('ascii')
    return pwdhash == storedPassword
