from ...models.funFact import FunFact
from ...utils import SessionMaker

class db:

    def __init__(self, Session):
        self.Session = Session

   # Create new account
    def add_fun_fact(self, body, netid):

        # Create account and profile
        sm = SessionMaker(self.Session)
        with sm as session:
            funFact = FunFact(
                netid   = netid,
                caption = body['caption'],
                photo   = body['photo']
            )
            session.add(funFact)
            session.commit()

            return funFact.id

    # Get fun facts
    def get_fun_facts(self, netid):
        sm = SessionMaker(self.Session)
        with sm as session:
            funFacts = session.query(FunFact).filter(FunFact.netid == netid).all()

            funFacts = [{ 'id'      : f.id,
                          'netid'   : f.netid,
                          'caption' : f.caption,
                          'photo'   : f.photo } for f in funFacts]
        return funFacts
