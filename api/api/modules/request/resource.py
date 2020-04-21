import ujson
from falcon import HTTPBadRequest, HTTP_200
from .db import db

class RequestResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    # Creates request
    def on_post(self, req, resp):

        # Make sure body exists
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Error loading request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Check request body
        sender      = body.get('sender')
        receiver    = body.get('receiver')

        # Check request body
        if sender is None or receiver is None:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Add request
        self.db.create_request(sender, receiver)

        # On success
        resp.status = HTTP_200

    # Updates request
    def on_put(self, req, resp):

        # Make sure body exists
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Error loading request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Check request body
        sender      = body.get('sender')
        receiver    = body.get('receiver')
        status      = body.get('status')

        if sender is None or receiver is None or status is None:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Add message
        self.db.update_request(sender, receiver, status)

        # On success
        resp.status = HTTP_200

    # Get all requests for a student
    def on_get(self, req, resp):

        if 'netid' not in req.params:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        resp.media = self.db.get_requests(req.params['netid'])
        resp.status = HTTP_200
