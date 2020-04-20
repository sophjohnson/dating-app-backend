import ujson
from falcon import HTTPBadRequest, HTTP_200
from ...utils import SessionMaker
from ...models.student import Student
from .db import db

class FunFactResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    def on_get(self, req, resp, netid):
        resp.media = self.db.get_fun_facts(netid)
        resp.status = HTTP_200

    # Creates fun fact
    def on_post(self, req, resp, netid):

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

        # Add student
        id = self.db.add_fun_fact(body, netid)

        # On success
        resp.media = {'funFactID': id}
        resp.status = HTTP_200

# Verify validity of request
def is_valid(body):
    valid = True
    necessaryParams = {
        'caption',
        'photo'
    }
    passedParams = set(body.keys())

    return necessaryParams == passedParams
