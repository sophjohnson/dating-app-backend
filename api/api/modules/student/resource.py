import ujson
from falcon import HTTPBadRequest, HTTP_200
from .db import db

class StudentResource(object):

    def __init__(self, Session):
        self.Session = Session
        self.db      = db(Session)

    def on_get(self, req, resp):
        resp.media = self.db.get_students()
        resp.status = HTTP_200

    # Creates student
    def on_post(self, req, resp):

        # Make sure body exists
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Must send request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Check request body
        if not is_valid(body):
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Check if student already exists
        if self.db.student_exists(body['netid']):
            msg = "Account with same netid already exists."
            raise HTTPBadRequest("Bad Request", msg)

        # Add student
        netid = self.db.create_student(body)

        # On success
        resp.media = {'netid': netid}
        resp.status = HTTP_200

    # Updates existing student
    def on_put(self, req, resp):

        # Make sure body exists
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Must send request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Check if student does not exists
        if not self.db.student_exists(body['netid']):
            msg = "No student exists for given netid."
            raise HTTPBadRequest("Bad Request", msg)

        # Add student
        netid = self.db.update_student(body)

        # On success
        resp.media = {'netid': netid}
        resp.status = HTTP_200

# Verify validity of request
def is_valid(body):
    necessaryParams = {
        'netid',
        'password',
        'firstName',
        'lastName',
        'gradYear',
        'city',
        'state',
        'dorm',
        'sexualOrientation',
        'genderIdentity'
    }
    passedParams = set(body.keys())

    return necessaryParams.issubset(passedParams)