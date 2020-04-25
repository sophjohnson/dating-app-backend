# Sophie Johnson

import falcon

from .modules.browse.resource import BrowseResource
from .modules.compatibility.resource import CompatibilityResource
from .modules.conversation.resource import ConversationResource
from .modules.dorm.resource import DormResource
from .modules.funFact.resource import FunFactResource, FunFactSpecificResource
from .modules.image.resource import ImageResource
from .modules.login.resource import LoginResource
from .modules.major.resource import MajorResource
from .modules.mass.resource import MassResource
from .modules.message.resource import MessageResource
from .modules.minor.resource import MinorResource
from .modules.recommendation.resource import RecommendationResource
from .modules.recommender.resource import RecommenderResource
from .modules.request.resource import RequestResource
from .modules.schedule.resource import ScheduleResource
from .modules.state.resource import StateResource
from .modules.student.resource import StudentResource, StudentSpecificResource

from.utils import CORSComponent

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def create_api():
    # Create engine
    engine = create_engine('oracle://guest:password@localhost:1521/XE')

    # Create sessionmaker
    Session = sessionmaker(bind=engine)

    # Create application
    api = application = falcon.API(middleware=[CORSComponent()])

    # Create instance for each resource
    browse          = BrowseResource(Session)
    compatibility   = CompatibilityResource(Session)
    conversation    = ConversationResource(Session)
    dorm            = DormResource(Session)
    funFact         = FunFactResource(Session)
    funFactSpecific = FunFactSpecificResource(Session)
    image           = ImageResource()
    login           = LoginResource(Session)
    major           = MajorResource(Session)
    mass            = MassResource(Session)
    message         = MessageResource(Session)
    minor           = MinorResource(Session)
    request         = RequestResource(Session)
    recommendation  = RecommendationResource(Session)
    recommender     = RecommenderResource(Session)
    schedule        = ScheduleResource(Session)
    state           = StateResource(Session)
    student         = StudentResource(Session)
    studentSpecific = StudentSpecificResource(Session)

    # Connect to resources
    api.add_route('/browse', browse)
    api.add_route('/compatibility', compatibility)
    api.add_route('/conversations/{netid}', conversation)
    api.add_route('/dorms', dorm)
    api.add_route('/funfacts/{netid}', funFact)
    api.add_route('/funfacts/{netid}/{id}', funFactSpecific)
    api.add_route('/images/{name}', image)
    api.add_route('/login', login)
    api.add_route('/majors', major)
    api.add_route('/masses', mass)
    api.add_route('/messages', message)
    api.add_route('/minors', minor)
    api.add_route('/requests', request)
    api.add_route('/recommendation', recommendation)
    api.add_route('/recommenders', recommender)
    api.add_route('/schedules/{netid}', schedule)
    api.add_route('/states', state)
    api.add_route('/students', student)
    api.add_route('/students/{netid}', studentSpecific)

    return api

application = create_api()
