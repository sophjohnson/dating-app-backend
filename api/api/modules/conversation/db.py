from ...models.conversation import Conversation
from ...models.message import Message
from ...utils import SessionMaker, format_time
from sqlalchemy import desc, and_

class db:

    def __init__(self, Session):
        self.Session = Session

    # Get id if conversation exists
    def conversation_exists(self, s1, s2):

        sm = SessionMaker(self.Session)
        with sm as session:
            id = session.query(Conversation.id)\
                        .filter(and_(Conversation.student1.like(s1), Conversation.student2.like(s2)))\
                        .scalar()
        return id

    # Create conversation
    def create_conversation(self, s1, s2):

        # Create conversation
        sm = SessionMaker(self.Session)
        with sm as session:
            conversation = Conversation(
                student1    = s1,
                student2    = s2
            )
            session.add(conversation)
            session.commit()

            return conversation.id

    # Get conversation id
    def get_conversation_id(self, s1, s2):

        # Alphabetical order
        (s1, s2) = sorted([s1, s2])

        # Get if exists, otherwise add
        id = self.conversation_exists(s1, s2)
        if id is None:
            id = self.create_conversation(s1, s2)

        return id

    # Get all conversations for given netid
    def get_conversations(self, netid):

        sm = SessionMaker(self.Session)
        with sm as session:
            # Get all conversations
            conversations = (session.query(Conversation.id, Conversation.student1.label("netid"))\
                                    .filter(Conversation.student2.like(netid)))\
                                    .union\
                            (session.query(Conversation.id, Conversation.student2.label("netid"))\
                                    .filter(Conversation.student1.like(netid)))\
                                    .all()

        conversations = [ self.get_details(c.id) for c in conversations]

        return conversations

    # Get all conversations for given netid
    def get_details(self, id):

        sm = SessionMaker(self.Session)
        with sm as session:
            lastMessage = session.query(Message)\
                                 .filter(Message.conversation == id)\
                                 .order_by(desc(Message.timestamp))\
                                 .first()

            details = {
                'sender'    : lastMessage.sender,
                'receiver'  : lastMessage.receiver,
                'content'   : lastMessage.content,
                'timestamp' : format_time(lastMessage.timestamp) }

        return details
