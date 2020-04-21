from ...models.recommender import Recommender
from ...models.student import Student
from ...utils import SessionMaker
from sqlalchemy import and_, desc
from falcon import HTTPBadRequest

class db:

    def __init__(self, Session):
        self.Session = Session

    # Check if already recommender
    def recommender_exists(self, recommender, recommendee):
        sm = SessionMaker(self.Session)
        with sm as session:
            recommender = session.query(Recommender)\
                                 .filter(and_(Recommender.recommender == recommender, Recommender.recommendee == recommendee))\
                                 .scalar()
            return recommender is not None

    # Create recommender (if it doesn't exist yet)
    def create_recommender(self, recommender, recommendee):

        # Check if already recommender
        if not self.recommender_exists(recommender, recommendee):

            sm = SessionMaker(self.Session)
            with sm as session:
                recommender = Recommender(
                    recommender     = recommender,
                    recommendee     = recommendee
                )
                session.add(recommender)
                session.commit()


    # Delete recommender
    def delete_recommender(self, recommender, recommendee):
        # Create account and profile
        sm = SessionMaker(self.Session)
        with sm as session:

            session.query(Recommender)\
                   .filter(and_(Recommender.recommender == recommender, Recommender.recommendee == recommendee))\
                   .delete()

            session.commit()

    # Get recommenders and recommendees
    def get_recommenders(self, netid):

        result = {}

        sm = SessionMaker(self.Session)
        with sm as session:

            # Get all recommenders
            recommenders = session.query(Recommender.recommender, Student.firstname, Student.lastname)\
                            .filter(Recommender.recommendee == netid)\
                            .join(Student, Recommender.recommender == Student.netid)\
                            .order_by(Student.firstname)\
                            .all()

            result['recommenders'] = [{  'netid'      : r.recommender,
                                         'firstName'  : r.firstname,
                                         'lastName'   : r.lastname } for r in recommenders ]

            # Get all recommendees
            recommendees = session.query(Recommender.recommendee, Student.firstname, Student.lastname)\
                            .filter(Recommender.recommender == netid)\
                            .join(Student, Recommender.recommendee == Student.netid)\
                            .order_by(Student.firstname)\
                            .all()

            result['recommendees'] = [{  'netid'      : r.recommendee,
                                         'firstName'  : r.firstname,
                                         'lastName'   : r.lastname } for r in recommendees ]

        return result
