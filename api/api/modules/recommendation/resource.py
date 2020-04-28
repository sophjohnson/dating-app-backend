import ujson
from falcon import HTTPBadRequest, HTTP_200
from .db import db
from ..student.db import db as sdb
from ..recommender.db import db as rdb
from ..compatibility.db import db as cdb

class RecommendationResource(object):

    def __init__(self, Session):
        self.db = db(Session)
        self.sdb = sdb(Session)
        self.rdb = rdb(Session)
        self.cdb = cdb(Session)

    # Updates status of recommendation
    def on_put(self, req, resp):

        # Make sure body exists
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Error loading request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Check request body
        viewer  = body.get('viewer')
        viewee  = body.get('viewee')
        status  = body.get('status')
        message = body.get('message')

        # Check request body
        if viewer is None or viewee is None or status is None:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Update request
        self.db.update_recommendation(viewer, viewee, status, message)

        # On success
        resp.status = HTTP_200

    # Get next recommendation
    def on_get(self, req, resp):

        # Check parameters
        netid = req.params.get('netid', None)
        if netid is None:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Get recommendation
        (recommendation, by) = self.db.get_recommendation(netid)

        # Find profile information
        if recommendation is not None:
             result = self.sdb.get_profile(recommendation)
             result['recommendedBy']    = by
             result['compatibility']    = self.cdb.get_compatibility_score(netid, recommendation)
             result['courses']          = len(self.cdb.get_courses(netid, recommendation))
             result['lunches']          = len(self.cdb.get_lunches(netid, recommendation))
             resp.media = result
        else:
            resp.media = {}

        resp.status = HTTP_200
