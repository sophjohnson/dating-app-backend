from ...models.browse import Browse
from ...models.student import Student
from ...models.preferences import Preferences
from ...models.recommendation import Recommendation
from ...models.major import Major
from ...models.minor import Minor
from ...utils import SessionMaker
from ..student.db import db as sdb
from ..compatibility.db import db as cdb
from sqlalchemy import and_, or_

class db:

    def __init__(self, Session):
        self.Session = Session
        self.sdb = sdb(Session)
        self.cdb = cdb(Session)

    # Create new browse record when viewer has made a decision
    def create_browse(self, viewedFor, netid, viewedBy):

        # Create browse
        sm = SessionMaker(self.Session)
        with sm as session:
            browse = Browse(
                viewedfor   = viewedFor,
                netid       = netid,
                viewedby    = viewedBy
            )
            session.add(browse)
            session.commit()

    # Get next profile to browse for given netid, by given netid
    def get_browse(self, params, viewFor, viewBy):

        # Get students based on preferences
        students = self.filter_preferences(params, viewFor, viewBy)

        # Get preferences for viewer
        sm = SessionMaker(self.Session)
        with sm as session:
            netid = session.query(Preferences).filter(Preferences.netid == viewFor).first()

        # Order by compatibility score
        student = max(students, key=lambda s: self.cdb.calculate_compatibility_score(netid, s))

        return student.netid, self.cdb.calculate_compatibility_score(netid, student)

    # Query to filter nonnegotiable preferences and given parameters
    def filter_preferences(self, params, viewFor, viewBy):

        sm = SessionMaker(self.Session)
        with sm as session:

            # Start building query
            query = session.query(Preferences)\
                           .join(Student.preferences)

            # Filter out existing recommendations and students who have been viewed before
            subquery = (session.query(Recommendation.viewee.label('netid'))\
                               .filter(Recommendation.viewer == viewFor))\
                               .union\
                       (session.query(Browse.netid.label('netid'))\
                               .filter(and_(Browse.viewedfor == viewFor, Browse.viewedby == viewBy)))

            query = query.filter(Student.netid.notin_(subquery))

            # Get target student's current preferences
            student = self.sdb.get_student(viewFor)
            identity = student['genderIdentity']
            orientation = student['sexualOrientation']

            # Gender identity/sexual orientation
            if identity == 'female' and orientation == 'heterosexual':
                query = query.filter(and_(Student.identity == 'male', or_(Student.orientation == 'heterosexual', Student.orientation == 'bisexual')))
            elif identity == 'female' and orientation == 'homosexual':
                query = query.filter(and_(Student.identity == 'female', or_(Student.orientation == 'homosexual', Student.orientation == 'bisexual')))
            elif identity == 'male' and orientation == 'heterosexual':
                query = query.filter(and_(Student.identity == 'female', or_(Student.orientation == 'heterosexual', Student.orientation == 'bisexual')))
            elif identity == 'male' and orientation == 'homosexual':
                query = query.filter(and_(Student.identity == 'male', or_(Student.orientation == 'homosexual', Student.orientation == 'bisexual')))

            # Filter by major
            major = params.pop('major', None)
            if major is not None:
                query = query.join(Student.majors)
                query = query.filter(Major.major == major)

            # Filter by minor
            minor = params.pop('minor', None)
            if minor is not None:
                query = query.join(Student.minors)
                query = query.filter(Minor.minor == minor)

            # Filter request parameters
            for attr, pref in params.items():
                actual = getattr(Student, attr)
                query = query.filter(pref == actual)

            return query.all()
