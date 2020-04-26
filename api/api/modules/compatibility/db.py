from falcon import HTTPBadRequest

from ...models.student import Student
from ...models.preferences import Preferences
from ...models.dorm import Dorm
from ...models.lunch import Lunch
from ...models.course import Course
from ...utils import SessionMaker, get_time_difference, format_time

class db:

    DISPLAY_DAYS = { 'MO' : 'Monday',
                     'TU' : 'Tuesday',
                     'WE' : 'Wednesday',
                     'TH' : 'Thursday',
                     'FR' : 'Friday' }

    def __init__(self, Session):
        self.Session = Session

    def get_courses(self, student1, student2):

        courses = []

        # Get students and preferences
        sm = SessionMaker(self.Session)
        with sm as session:
            s1Courses = session.query(Course)\
                        .join(Student.courses)\
                        .filter(Student.netid == student1).all()
            s2Courses = session.query(Course)\
                        .join(Student.courses)\
                        .filter(Student.netid == student2).all()

        for s1c in s1Courses:
            for s2c in s2Courses:
                if s1c.id == s2c.id:
                    courses.append(s1c.course)

        return courses

    def get_lunches(self, student1, student2):

        lunches = []

        # Get students and preferences
        sm = SessionMaker(self.Session)
        with sm as session:
            s1Lunches = session.query(Lunch)\
                        .join(Student.lunches)\
                        .filter(Student.netid == student1).all()
            s2Lunches = session.query(Lunch)\
                        .join(Student.lunches)\
                        .filter(Student.netid == student2).all()

        for s1l in s1Lunches:
            for s2l in s2Lunches:
                if s1l.day == s2l.day:
                    lunch = self.find_lunch_overlap(s1l, s2l)
                    if lunch is not None:
                        lunches.append('{} from {}'.format(self.DISPLAY_DAYS[s1l.day], lunch))

        return lunches

    # See if overlap at least an hour long
    def find_lunch_overlap(self, s1, s2):
        lunch   = None
        start   = max(s1.starttime.time(), s2.starttime.time())
        end     = min(s1.endtime.time(), s2.endtime.time())
        if get_time_difference(end, start) >= 60:
            return '{} - {}'.format(format_time(start), format_time(end))

    # Find all similar interests
    def get_messages(self, student1, student2):

        messages = []

        # Get students and preferences
        sm = SessionMaker(self.Session)
        with sm as session:
            s1 = session.query(Student, Preferences, Dorm)\
                        .join(Student.preferences)\
                        .join(Student.studentdorm)\
                        .filter(Student.netid == student1).first()
            s2 = session.query(Student, Preferences, Dorm)\
                        .join(Student.preferences)\
                        .join(Student.studentdorm)\
                        .filter(Student.netid == student2).first()

            if s1 is None or s2 is None:
                msg = "Given students do not exist."
                raise HTTPBadRequest("Bad Request", msg)

        (s1, s1Pref, s1Dorm) = s1
        (s2, s2Pref, s2Dorm) = s2

        messages.append('Go {}, amirite?!'.format(s2Dorm.mascot))

        # Live on same quad
        if s1Dorm.quad == s2Dorm.quad:
            messages.append('{}, best quad!'.format(s1Dorm.quad))

        # Dining hall preferences
        if s1Pref.dininghall == s2Pref.dininghall:
            messages.append('How about that food at {} today?'.format(s1Pref.dininghall))
        else:
            messages.append('Okay, real talk... {} > {}'.format(s1Pref.dininghall, s2Pref.dininghall))


        return messages

    # Use algorithm to find compatibility score
    def get_compatibility_score(self, student1, student2):

        # Get students and preferences
        sm = SessionMaker(self.Session)
        with sm as session:
            s1 = session.query(Preferences).filter(Preferences.netid == student1).first()
            s2 = session.query(Preferences).filter(Preferences.netid == student2).first()

        if s1 is None or s2 is None:
            msg = "Given students do not exist."
            raise HTTPBadRequest

        return self.calculate_compatibility_score(s1, s2)

    # Calculate compatibility given preferences objects
    def calculate_compatibility_score(self, s1, s2):

        compatibility = 0

        if s1.temperament == s2.idealtemperament:
            compatibility += 3
        if s1.giveaffection == s2.receiveaffection:
            compatibility += 3
        if s1.trait == s2.idealtrait:
            compatibility += 3
        if s1.idealdate == s2.idealdate:
            compatibility += 2
        if s1.fridaynight == s2.fridaynight:
            compatibility += 2
        if s1.dininghall == s2.dininghall:
            compatibility += 1
        if s1.studyspot == s2.studyspot:
            compatibility += 1
        if s1.mass == s2.mass:
            compatibility += 3
        if s1.club == s2.club:
            compatibility += 2
        if s1.gameday == s2.gameday:
            compatibility += 2
        if s1.hour == s2.hour:
            compatibility += 1
        if s1.idealtemperament == s2.temperament:
            compatibility += 3
        if s1.receiveaffection == s2.giveaffection:
            compatibility += 3
        if s1.idealtrait == s2.trait:
            compatibility += 3

        return round(compatibility / 32, 4) * 100