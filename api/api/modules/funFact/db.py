import os
from sqlalchemy import and_

from ..image.resource import ImageHandler
from ...models.funFact import FunFact
from ...utils import SessionMaker

class db:

    def __init__(self, Session):
        self.Session = Session
        self.ImageHandler = ImageHandler(os.path.dirname(__file__))

   # Create new fun fact
    def add_fun_fact(self, req, netid):

        id = None

        # Create fun fact
        sm = SessionMaker(self.Session)
        with sm as session:
            funFact = FunFact(
                netid   = netid,
                caption = req.params['caption']
            )
            session.add(funFact)
            session.commit()

            id = funFact.id

        # Save image
        imagePath = self.ImageHandler.save_image(req, netid, id)

        # Update fun fact with image path
        sm = SessionMaker(self.Session)
        with sm as session:
            session.query(FunFact)\
                   .filter(FunFact.id == id)\
                   .update({'image': imagePath})
            session.commit()

        # Update image path if successful
        return funFact.id

    # Get fun facts
    def get_fun_facts(self, netid):
        sm = SessionMaker(self.Session)
        with sm as session:
            funFacts = session.query(FunFact).filter(FunFact.netid == netid).all()

            funFacts = [{ 'id'      : f.id,
                          'netid'   : f.netid,
                          'caption' : f.caption,
                          'image'   : f.image } for f in funFacts]
        return funFacts

    # Update existing fun fact
    def update_fun_fact(self, req, netid, id):
        sm = SessionMaker(self.Session)
        with sm as session:

            # Save image
            imagePath = self.ImageHandler.save_image(req, netid, id)

            # Update fun fact
            funFact = session.query(FunFact)\
                             .filter(and_(FunFact.id == id, FunFact.netid == netid))\
                             .first()

            # If fun fact doesn't exist
            if funFact is None:
                msg = "No funFact exists for given id and netid."
                raise HTTPBadRequest("Bad Request", msg)

            # Handle update caption
            funFact.caption = req.params['caption']
            funFact.image   = imagePath

            session.commit()

        return id

    # Delete existing fun fact
    def delete_fun_fact(self, netid, id):
        sm = SessionMaker(self.Session)
        with sm as session:

            image = session.query(FunFact.image).filter(FunFact.id == id).scalar()

            if self.ImageHandler.delete_image(image):
                funFact = session.query(FunFact)\
                                 .filter(and_(FunFact.id == id, FunFact.netid == netid))\
                                 .delete()

                session.commit()
            else:
                return False

        return True
