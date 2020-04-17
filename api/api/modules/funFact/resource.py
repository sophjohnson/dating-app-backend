import ujson
from falcon import HTTPBadRequest, HTTP_200
from ...utils import SessionMaker
from ...models.student import Student
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
        netid = self.db.add_student(body)
    
        # On success
        resp.media = {'netid': netid}
        resp.status = HTTP_200

# Verify validity of request
def is_valid(body):
    valid = True
    necessaryParams = {
        'netid',
        'password'
    }
    passedParams = set(body.keys())

    return necessaryParams.issubset(passedParams)

