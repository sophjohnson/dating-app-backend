import ujson
from falcon import HTTPBadRequest, HTTP_200
from .db import db

class LoginResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    # Checks netid and password
    def on_post(self, req, resp):

        # Read body
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Must send request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Check body parameters
        netid       = body['netid']
        password    = body['password']

        if netid is None or password is None:
            msg = "Must provide netid and password."
            raise HTTPBadRequest("Bad Request", msg)

        # Validate netid and password combination
        result = self.db.validate(netid, password)

        resp.media = {'Title': 'Correct password'}
        resp.status = HTTP_200

    # Updates password
    def on_put(self, req, resp):

        # Read body
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Must send request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Check body parameters
        netid   = body.get('netid')
        old     = body.get('oldPassword')
        new     = body.get('newPassword')

        if netid is None or old is None or new is None:
            msg = "Must provide netid, oldPassword, and newPassword."
            raise HTTPBadRequest("Bad Request", msg)

        # Validate netid and password combination
        if self.db.validate(netid, old):
            self.db.update_password(netid, new)

        resp.media = {'netid': netid}
        resp.status = HTTP_200
