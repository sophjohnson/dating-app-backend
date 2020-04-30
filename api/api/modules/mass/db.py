from ...models.mass import Mass 
from ...utils import SessionMaker

class db:

    DAYS = {'Sunday'    : 0,
            'Monday'    : 1,
            'Tuesday'   : 2,
            'Wednesday' : 3,
            'Thursday'  : 4,
            'Friday'    : 5,
            'Saturday'  : 6 }

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

        masses = sorted(masses, key=lambda mass: self.DAYS[mass['day']])

        return masses 
