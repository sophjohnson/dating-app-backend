# Sophie Johnson

import falcon

from .modules.conversation.resource import ConversationResource
from .modules.dorm.resource import DormResource
from .modules.major.resource import MajorResource
from .modules.mass.resource import MassResource
from .modules.message.resource import MessageResource
from .modules.minor.resource import MinorResource
from .modules.state.resource import StateResource
from .modules.student.resource import StudentResource

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_api():
    # Create engine
    engine = create_engine('oracle://guest:password@localhost:1521/XE')

    # Create sessionmaker
    Session = sessionmaker(bind=engine)

    # Create application
    api = application = falcon.API()

    # Create instance for each resource
    conversation    = ConversationResource(Session)
    dorm            = DormResource(Session)
    major           = MajorResource(Session)
    mass            = MassResource(Session)
    message         = MessageResource(Session)
    minor           = MinorResource(Session)
    state           = StateResource(Session)
    student         = StudentResource(Session)

    # Connect to resources
    api.add_route('/conversations/{netid}', conversation)
    api.add_route('/dorms', dorm)
    api.add_route('/majors', major)
    api.add_route('/masses', mass)
    api.add_route('/messages', message)
    api.add_route('/minors', minor)
    api.add_route('/states', state)
    api.add_route('/students', student)

    return api

application = create_api()
