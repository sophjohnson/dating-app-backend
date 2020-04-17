from ...models.minor import Minor 
from ...utils import SessionMaker

class db:

    def __init__(self, Session):
        self.Session = Session

    # Get minors 
    def get_minors(self):

        sm = SessionMaker(self.Session)
        with sm as session:
            minors = session.query(Minor).all()
            minors = [ s.minor for s in minors]

        return minors 
