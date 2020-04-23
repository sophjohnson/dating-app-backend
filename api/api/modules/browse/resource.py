import ujson
from falcon import HTTPBadRequest, HTTP_200
from .db import db
from ..student.db import db as sdb

class BrowseResource(object):

    def __init__(self, Session):
        self.db = db(Session)
        self.sdb = sdb(Session)

    # Get next profile in browse
    def on_get(self, req, resp):

        # Check parameters
        viewFor = req.params.pop('viewFor', None)
        viewBy  = req.params.pop('viewBy', None)

        if viewFor is None or viewBy is None:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Get next profile to browse
        netid = None
        students = self.db.get_browse(req.params, viewFor, viewBy)

        # Find profile information
        if netid is not None:
             resp.media = self.sdb.get_profile(netid)
        else:
            resp.media = students

        resp.status = HTTP_200
