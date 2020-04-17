import falcon
from .db import db

class MassResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    # Get all masses
    def on_get(self, req, resp):

            resp.media = self.db.get_masses()
            resp.status = falcon.HTTP_200
