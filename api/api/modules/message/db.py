from ...models.message import Message
from ...utils import SessionMaker, get_curr_time
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


#conversations = [{  'id'        : c.id,
#                    'sender'    : c.sender,
#                    'receiver'  : c.receiver,
#                    'content'   : c.content,
#                    'timestamp' : format_time(c.timestamp) } for c in conversations]
