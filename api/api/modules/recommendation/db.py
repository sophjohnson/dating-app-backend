from ...models.recommendation import Recommendation
from ...utils import SessionMaker, get_curr_time
from ..message.db import db as mdb
from falcon import HTTPBadRequest
from sqlalchemy import and_

class db:

    def __init__(self, Session):
        self.Session = Session
        self.mdb = mdb(Session)

    # Determine if recommendation exists
    def recommendation_exists(self, viewer, viewee):

        sm = SessionMaker(self.Session)
        with sm as session:
            recommendation = session.query(Recommendation)\
                                    .filter(and_(Recommendation.viewer == viewer, Recommendation.viewee == viewee))\
                                    .scalar()
        return recommendation is not None

    # Create recommendation
    def create_recommendation(self, viewer, viewee, netid):

        if not self.recommendation_exists(viewer, viewee):
            # Create recommendation
            sm = SessionMaker(self.Session)
            with sm as session:
                recommendation = Recommendation(
                    viewer          = viewer,
                    viewee          = viewee,
                    status          = 'pending',
                    recommendedby   = netid,
                    timestamp       = get_curr_time()
                )
                session.add(recommendation)
                session.commit()

   # Update existing recommendation
    def update_recommendation(self, viewer, viewee, status, message):

        # Create account and profile
        sm = SessionMaker(self.Session)
        with sm as session:

            recommendation = session.query(Recommendation)\
                                    .filter(and_(Recommendation.viewer == viewer, Recommendation.viewee == viewee))\
                                    .scalar()

            # If recommendation doesn't exist
            if recommendation is None:
                msg = "No recommendation for given netids exists."
                raise HTTPBadRequest("Bad Request", msg)

            # Send message (if interested)
            if status == "interested" and message:
                self.mdb.create_message(viewer, viewee, message)

            # Update status
            recommendation.status = status

            session.commit()

            return recommendation.status

    # Get next recommendations for given netid
    def get_recommendation(self, netid):

        sm = SessionMaker(self.Session)
        with sm as session:
            # Get all conversations
            recommendation = session.query(Recommendation.viewee, Recommendation.recommendedby)\
                                    .filter(and_(Recommendation.viewer == netid, Recommendation.status == 'pending'))\
                                    .order_by(Recommendation.timestamp)\
                                    .first()

            if recommendation is None:
                return None

            return recommendation.viewee, recommendation.recommendedby
