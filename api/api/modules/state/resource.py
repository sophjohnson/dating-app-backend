import falcon
from .db import db

class StateResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    # Get all state names and abbreviations
    def on_get(self, req, resp):

        resp.media = self.db.get_states() 
        resp.status = falcon.HTTP_200
