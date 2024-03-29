from ...models.conversation import Conversation
from ...models.student import Student
from ...models.message import Message
from ...utils import SessionMaker, format_datetime
from sqlalchemy import desc, and_

class db:

    def __init__(self, Session):
        self.Session = Session

    # Get id if conversation exists
    def conversation_exists(self, s1, s2):

        # Alphabetical order
        (s1, s2) = sorted([s1, s2])

        sm = SessionMaker(self.Session)
        with sm as session:
            id = session.query(Conversation.id)\
                        .filter(and_(Conversation.student1 == s1, Conversation.student2 == s2))\
                        .scalar()
        return id

    # Create conversation
    def create_conversation(self, s1, s2):

        # Alphabetical order
        (s1, s2) = sorted([s1, s2])

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

    # Get all conversations for given netid
    def get_conversations(self, netid):

        sm = SessionMaker(self.Session)
        with sm as session:
            # Get all conversations
            conversations = (session.query(Conversation.id, Conversation.student1.label('netid'), Student.firstname.label('first'), Student.lastname.label('last'), Student.image.label('image'))\
                                    .join(Student, Student.netid == Conversation.student1)\
                                    .filter(Conversation.student2 == netid))\
                                    .union\
                            (session.query(Conversation.id, Conversation.student2.label('netid'), Student.firstname.label('first'), Student.lastname.label('last'), Student.image.label('image'))\
                                    .join(Student, Student.netid == Conversation.student2)\
                                    .filter(Conversation.student1 == netid))\
                                    .all()

        conversations = [ self.get_details(c) for c in conversations]
        conversations = sorted(conversations, key = lambda c: c['timestamp'], reverse=True)

        return conversations

    # Get all conversations for given netid
    def get_details(self, c):

        sm = SessionMaker(self.Session)
        with sm as session:
            lastMessage = session.query(Message)\
                                 .filter(Message.conversation == c.id)\
                                 .order_by(desc(Message.timestamp))\
                                 .first()

            details = {
                'id'        : c.id,
                'netid'     : c.netid,
                'firstName' : c.first,
                'lastName'  : c.last,
                'image'     : c.image,
                'sender'    : lastMessage.sender,
                'receiver'  : lastMessage.receiver,
                'content'   : lastMessage.content,
                'timestamp' : format_datetime(lastMessage.timestamp) }

        return details
