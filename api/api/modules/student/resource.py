import ujson
from falcon import HTTPBadRequest, HTTP_200
from .db import db

class StudentResource(object):

    def __init__(self, Session):
        self.Session = Session
        self.db      = db(Session)

    # Creates student
    def on_post(self, req, resp):

        # Make sure body exists
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Error loading request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Verify contents of body
        netid = body.get('netid', None)
        password = body.get('password', None)

        if netid is None or password is None:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Check if student already exists
        if self.db.student_exists(netid):
            msg = "Student with same netid already exists."
            raise HTTPBadRequest("Bad Request", msg)

        # Add student
        netid = self.db.create_student(netid, password)

        # On success
        resp.media = {'netid': netid}
        resp.status = HTTP_200

class StudentSpecificResource(object):

    def __init__(self, Session):
        self.Session = Session
        self.db      = db(Session)

    def on_get(self, req, resp, netid):
        resp.media = self.db.get_student(netid)
        resp.status = HTTP_200

    # Updates existing student
    def on_put(self, req, resp, netid):

        # Make sure body exists
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Must send request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Check request body
        if not is_valid(body):
            msg = "Contains incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Add student
        netid = self.db.update_student(body, netid)

        # On success
        resp.media = {'netid': netid}
        resp.status = HTTP_200

    # Add/update profile picture
    def on_post(self, req, resp, netid):

        # Update student image
        netid = self.db.update_image(req, netid)

        # On success
        resp.media = {'netid': netid}
        resp.status = HTTP_200

# Verify validity of request
def is_valid(body):
    necessaryParams = {
        'firstName',
        'lastName',
        'gradYear',
        'majors',
        'minors',
        'city',
        'state',
        'dorm',
        'genderIdentity',
        'browseGenderIdentity',
        'question',
        'danceInvite',
        'temperament',
        'giveAffection',
        'trait',
        'idealDate',
        'fridayNight',
        'diningHall',
        'studySpot',
        'mass',
        'club',
        'gameDay',
        'hour',
        'zodiacSign',
        'idealTemperament',
        'receiveAffection',
        'idealTrait'
    }
    passedParams = set(body.keys())

    return passedParams.issubset(necessaryParams)
