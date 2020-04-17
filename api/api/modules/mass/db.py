from ...models.mass import Mass 
from ...utils import SessionMaker

class db:

    def __init__(self, Session):
        self.Session = Session

    # Get masses 
    def get_masses(self):
        sm = SessionMaker(self.Session)
        with sm as session:
            masses = session.query(Mass).all()
            masses = [{ 'massID'    : s.massid,
                        'location'  : s.location,
                        'day'       : s.day,
                        'time'      : s.time } for s in masses]

        return masses 
