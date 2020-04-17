import falcon

from ...models.dorm import Dorm
from .db import db

class DormResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    # Get list of all dorm info
    def on_get(self, req, resp):

            resp.media = self.db.get_dorms() 
            resp.status = falcon.HTTP_200
