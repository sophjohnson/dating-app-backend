import falcon
from .db import db

class MinorResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    # Get all minor names
    def on_get(self, req, resp):

        resp.media = self.db.get_minors()
        resp.status = falcon.HTTP_200
