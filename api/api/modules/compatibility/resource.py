from falcon import HTTPBadRequest, HTTP_200
from .db import db

class CompatibilityResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    # Get points of similarity
    def on_get(self, req, resp):

        viewer  = req.params.get('viewer')
        viewee  = req.params.get('viewee')

        if viewer is None or viewee is None:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        response = {}

        response['compatibility']   = self.db.get_compatibility_score(viewer, viewee)
        response['courses']         = self.db.get_courses(viewer, viewee)
        response['lunches']         = self.db.get_lunches(viewer, viewee)
        response['messages']        = self.db.get_messages(viewer, viewee)

        resp.media = response
        resp.status = HTTP_200
