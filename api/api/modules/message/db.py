from ...models.message import Message
from ...models.student import Student
from ...utils import SessionMaker, get_curr_time, get_earliest_time, format_datetime
from ..conversation.db import db as cdb

class db:

    def __init__(self, Session):
        self.Session = Session
        self.cdb = cdb(Session)

    # Create message
    def create_message(self, sender, receiver, content):


        # Get conversaion id (if exists)
        id = self.cdb.conversation_exists(sender, receiver)

        # Get id if new conversation, record if first message
        firstMessage = False
        if id is None:
            firstMessage = True
            id = self.cdb.create_conversation(sender, receiver)

        sm = SessionMaker(self.Session)
        with sm as session:

            # Add prompt question if first message in conversation
            if firstMessage:

                question = session.query(Student.question).filter(Student.netid == receiver).scalar()
                print(question)
                message = Message(
                    conversation    = id,
                    sender          = receiver,
                    receiver        = sender,
                    content         = question,
                    timestamp       = get_earliest_time()
                )
                session.add(message)
                session.commit()

            # Add actual message
            message = Message(
                conversation    = id,
                sender          = sender,
                receiver        = receiver,
                content         = content,
                timestamp       = get_curr_time()
            )
            session.add(message)
            session.commit()

            return message.id

    # Get messages from conversation
    def get_messages(self, id):
        sm = SessionMaker(self.Session)
        with sm as session:

            # Get last 20 messages
            messages = session.query(Message)\
                              .filter(Message.conversation == id)\
                              .order_by(Message.timestamp)\
                              .limit(20)\
                              .all()

            messages = [{  'id'        : m.id,
                           'sender'    : m.sender,
                           'receiver'  : m.receiver,
                           'content'   : m.content,
                           'timestamp' : format_datetime(m.timestamp) } for m in messages ]

        return messages
