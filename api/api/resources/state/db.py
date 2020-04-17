from ...models.state import State 
from ...utils import SessionMaker

class db:

    def __init__(self, Session):
        self.Session = Session

    # Get states 
    def get_states(self):

        sm = SessionMaker(self.Session)
        with sm as session:
            states = session.query(State).all()
            states = [{ 'code' : s.code,
                        'name' : s.state } for s in states]

        return states 
