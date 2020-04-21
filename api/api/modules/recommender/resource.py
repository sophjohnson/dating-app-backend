import ujson
from falcon import HTTPBadRequest, HTTP_200
from .db import db

class RecommenderResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    # Deletes recommender relationship
    def on_delete(self, req, resp):

        # Make sure body exists
        try:
            body = ujson.loads(req.stream.read())
        except ValueError:
            msg = "Error loading request body."
            raise HTTPBadRequest("Bad Request", msg)

        # Check request body
        recommender = body.get('recommender')
        recommendee = body.get('recommendee')

        if recommender is None or recommendee is None:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        # Delete recommender relationship
        self.db.delete_recommender(recommender, recommendee)

        # On success
        resp.status = HTTP_200

    # Get all recommenders AND recommendees for a student
    def on_get(self, req, resp):

        if 'netid' not in req.params:
            msg = "Missing or incorrect parameters."
            raise HTTPBadRequest("Bad Request", msg)

        resp.media = self.db.get_recommenders(req.params['netid'])
        resp.status = HTTP_200
