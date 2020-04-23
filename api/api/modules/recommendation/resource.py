import ujson
from falcon import HTTPBadRequest, HTTP_200
from .db import db
from ..student.db import db as sdb
from ..recommender.db import db as rdb

class RecommendationResource(object):

    def __init__(self, Session):
        self.db = db(Session)
        self.sdb = sdb(Session)
        self.rdb = rdb(Session)

    # Creates recommendation
    def on_post(self, req, resp):

        # Make sure body exists
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Error loading request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Check request body
        viewer  = body.get('viewer')
        viewee  = body.get('viewee')
        netid   = body.get('recommendedBy')

        # Check request body
        if viewer is None or viewee is None or netid is None:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Verify valid recommender
        if not self.rdb.recommender_exists(netid, viewer):
            msg = "Unapproved recommender."
            raise HTTPBadRequest("Bad Request", msg)

        # Add request
        self.db.create_recommendation(viewer, viewee, netid)

        # On success
        resp.status = HTTP_200

    # Updates status recommendation
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
        if 'netid' not in req.params:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Get recommendation
        recommendation = self.db.get_recommendation(req.params['netid'])

        # Find profile information
        if recommendation is not None:
             result = self.sdb.get_profile(recommendation[0])
             result['recommendedBy'] = recommendation[1]
             resp.media = result
        else:
            resp.media = {}

        resp.status = HTTP_200
