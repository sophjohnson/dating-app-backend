import binascii
import hashlib
import os
import uuid

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
            dorms = [{ 'dorm'               : s.dorm,
                       'mascot'             : s.mascot,
                       'quad'               : s.quad,
                       'logo'               : s.logo,
                       'airConditioning'    : s.airconditioning } for s in dorms]
        return dorms
