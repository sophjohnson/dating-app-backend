from ...models.request import Request
from ...models.student import Student
from ...utils import SessionMaker, get_curr_time, format_time
from ..recommender.db import db as rdb
from sqlalchemy import and_, desc
from falcon import HTTPBadRequest

class db:

    def __init__(self, Session):
        self.Session = Session
        self.rdb = rdb(Session)

    def request_exists(self, sender, receiver):
        sm = SessionMaker(self.Session)
        with sm as session:
            request = session.query(Request)\
                             .filter(and_(Request.sender == sender, Request.receiver == receiver))\
                             .scalar()
            return request is not None

    # Create request (if it doesn't exist yet)
    def create_request(self, sender, receiver):

        if not self.request_exists(sender, receiver):

            sm = SessionMaker(self.Session)
            with sm as session:
                request = Request(
                    sender          = sender,
                    receiver        = receiver,
                    timestamp       = get_curr_time()
                )
                session.add(request)
                session.commit()

                return request.status

    # Either accept or reject request
    def update_request(self, sender, receiver, status):

        # If request does not exist
        if not self.request_exists(sender, receiver):
            msg = 'Request does not exist.'
            raise HTTPBadRequest("Bad Request", msg)

        if status == 'accept':
            self.rdb.create_recommender(receiver, sender)
        elif status != 'reject':
            msg = "Updated status must be accept or reject."
            raise HTTPBadRequest("Bad Request", msg)

        # Delete request (both for accept and reject)
        self.delete_request(sender, receiver)

    # Delete request (after accepted/rejected)
    def delete_request(self, sender, receiver):
        # Create account and profile
        sm = SessionMaker(self.Session)
        with sm as session:

            session.query(Request)\
                   .filter(and_(Request.sender == sender, Request.receiver == receiver))\
                   .delete()

            session.commit()

    # Get requests from conversation
    def get_requests(self, netid):
        sm = SessionMaker(self.Session)
        with sm as session:

            # Get all requests
            requests = session.query(Request.sender, Student.firstname, Student.lastname)\
                            .filter(Request.receiver == netid)\
                            .join(Student, Request.sender == Student.netid)\
                            .order_by(desc(Request.timestamp))\
                            .all()

            requests = [{  'sender'     : r.sender,
                           'firstName'  : r.firstname,
                           'lastName'   : r.lastname } for r in requests ]

        return requests
