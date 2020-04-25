import ujson
from falcon import HTTPBadRequest, HTTP_200
from .db import db

class ScheduleResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    # Parse student's .ics file
    def on_post(self, req, resp, netid):

        # Update student image
        courses = self.db.parse_schedule(req, netid)

        # On success
        resp.media = {'courses': courses}
        resp.status = HTTP_200
