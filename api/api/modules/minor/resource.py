import falcon

class MinorResource(object):

    def __init__(self, Session):
        self.Session = Session

    # Get all minor names
    def on_get(self, req, resp):

        resp.media = self.db.get_minors() 
        resp.status = falcon.HTTP_200
