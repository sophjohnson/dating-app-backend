# Sophie Johnson

import falcon

from .resources.dorm.resource import DormResource
from .resources.major.resource import MajorResource 
from .resources.mass.resource import MassResource 
from .resources.minor.resource import MinorResource 
from .resources.state.resource import StateResource 
from .resources.student.resource import StudentResource

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
    dorm = DormResource(Session)
    minor = MinorResource(Session)
    major = MajorResource(Session)
    mass = MassResource(Session)
    state = StateResource(Session)
    student = StudentResource(Session)

    # Connect to resources
    api.add_route('/dorms', dorm)
    api.add_route('/majors', major)
    api.add_route('/masses', mass)
    api.add_route('/minors', minor)
    api.add_route('/states', state)
    api.add_route('/students', student)

    return api

application = create_api()
