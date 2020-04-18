from ...models.dorm import Dorm
from ...utils import SessionMaker

class db:

    def __init__(self, Session):
        self.Session = Session

    # Get dorms
    def get_dorms(self):
        sm = SessionMaker(self.Session)
        with sm as session:
            dorms = session.query(Dorm).all()
            dorms = [{ 'dorm'               : d.dorm,
                       'mascot'             : d.mascot,
                       'quad'               : d.quad,
                       'logo'               : d.logo,
                       'airConditioning'    : d.airconditioning } for d in dorms]
        return dorms
