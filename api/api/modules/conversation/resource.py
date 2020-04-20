import ujson
from falcon import HTTPBadRequest, HTTP_200
from .db import db

class ConversationResource(object):

    def __init__(self, Session):
        self.db = db(Session)

    # Get all conversations
    def on_get(self, req, resp, netid):
        resp.media = self.db.get_conversations(netid)
        resp.status = HTTP_200
