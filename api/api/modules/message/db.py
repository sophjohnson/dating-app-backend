from ...models.message import Message
from ...utils import SessionMaker, get_curr_time, format_time
from ..conversation.db import db as conversation_db

class db:

    def __init__(self, Session):
        self.Session = Session
        self.cdb = conversation_db(Session)

    # Create message
    def create_message(self, body):

        # Create or get conversation id
        id = self.cdb.get_conversation_id(body['sender'], body['receiver'])

        # Create account and profile
        sm = SessionMaker(self.Session)
        with sm as session:
            message = Message(
                conversation    = id,
                sender          = body['sender'],
                receiver        = body['receiver'],
                content         = body['content'],
                timestamp       = get_curr_time()
            )
            session.add(message)
            session.commit()

            return message.id

    # Get messages from conversation
    def get_messages(self, params):
        sm = SessionMaker(self.Session)
        with sm as session:

            # Get conversation id
            id = self.cdb.get_conversation_id(params['sender'], params['receiver'])

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
                           'timestamp' : format_time(m.timestamp) } for m in messages ]

        return messages
