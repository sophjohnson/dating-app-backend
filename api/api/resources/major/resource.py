import falcon
from .db import db

class MajorResource(object):

    def __init__(self, Session):
        self.db = db(Session) 

    # Get list of majors
    def on_get(self, req, resp):

        resp.media = self.db.get_majors()
        resp.status = falcon.HTTP_200
