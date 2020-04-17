from ...models.major import Major 
from ...utils import SessionMaker

class db:

    def __init__(self, Session):
        self.Session = Session

    # Get majors 
    def get_majors(self):

        sm = SessionMaker(self.Session)
        with sm as session:
            majors = session.query(Major).all()
            majors = [ s.major for s in majors]

        return majors
