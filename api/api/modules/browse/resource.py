import ujson
from falcon import HTTPBadRequest, HTTP_200
from .db import db
from ..student.db import db as sdb
from ..recommender.db import db as rdb
from ..recommendation.db import db as rndb

class BrowseResource(object):

    def __init__(self, Session):
        self.db = db(Session)
        self.sdb = sdb(Session)
        self.rdb = rdb(Session)
        self.rndb = rndb(Session)

    # Update based on response to given profile
    def on_post(self, req, resp):

        # Make sure body exists
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Error loading request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Check request body
        viewedFor   = body.get('viewedFor', None)
        netid       = body.get('netid', None)
        viewedBy    = body.get('viewedBy', None)
        status      = body.get('status', None)

        if viewedFor is None or netid is None or viewedBy is None or status is None:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Verify valid recommender
        if not self.rdb.recommender_exists(viewedBy, viewedFor):
            msg = "Unapproved recommender."
            raise HTTPBadRequest("Bad Request", msg)

        # If recommend, then create recommendation
        if status == 'recommend':
            self.rndb.create_recommendation(viewedFor, netid, viewedBy)

        self.db.create_browse(viewedFor, netid, viewedBy)

        # On success
        resp.status = HTTP_200

    # Get next profile in browse
    def on_get(self, req, resp):

        # Check parameters
        viewFor = req.params.pop('viewFor', None)
        viewBy  = req.params.pop('viewBy', None)

        if viewFor is None or viewBy is None:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Verify valid recommender
        if not self.rdb.recommender_exists(viewBy, viewFor):
            msg = "Unapproved recommender."
            raise HTTPBadRequest("Bad Request", msg)

        # Get next profile to browse
        netid = self.db.get_browse(req.params, viewFor, viewBy)

        # Find profile information
        if netid is not None:
             resp.media = self.sdb.get_profile(netid)

        resp.status = HTTP_200
