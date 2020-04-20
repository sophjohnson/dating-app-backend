import ujson
from falcon import HTTPBadRequest, HTTPError, HTTP_200
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

        if 'caption' not in req.params:
            msg = "Must send caption."
            raise HTTPBadRequest("Bad Request", msg)

        # Add fun fact
        id = self.db.add_fun_fact(req, netid)

        # On success
        resp.media = {'funFactID': id}
        resp.status = HTTP_200

class FunFactSpecificResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    # Updates existing fun fact
    def on_put(self, req, resp, netid, id):

        if 'caption' not in req.params:
            msg = "Must send caption."
            raise HTTPBadRequest("Bad Request", msg)

        # Update fun fact
        id = self.db.update_fun_fact(req, netid, id)

        resp.media = {'funFactID': id}
        resp.status = HTTP_200

    # Delete fun fact
    def on_delete(self, req, resp, netid, id):
        if not self.db.delete_fun_fact(netid, id):
            msg = "Failed to delete fun fact."
            raise HTTPError("Error", msg)

        resp.media = {'deletedFunFact': id}
        resp.status = HTTP_200
