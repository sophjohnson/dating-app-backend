import ujson
from falcon import HTTPBadRequest, HTTP_200
from .db import db

class MessageResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    # Creates message
    def on_post(self, req, resp):

        # Make sure body exists
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Must send request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Check request body
        if not is_valid(body):
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Add message
        id = self.db.create_message(body['sender'], body['receiver'], body['content'])

        # On success
        resp.media = {'id': id}
        resp.status = HTTP_200

    # Get all messages in a conversation
    def on_get(self, req, resp):
        if 'id' not in req.params:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        resp.media = self.db.get_messages(req.params['id'])
        resp.status = HTTP_200


# Verify validity of request
def is_valid(body):
    necessaryParams = {
        'sender',
        'receiver',
        'content'
    }
    passedParams = set(body.keys())

    return necessaryParams == passedParams
