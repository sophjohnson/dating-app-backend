from falcon import HTTPBadRequest

from ...models.student import Student
from ...models.preferences import Preferences
from ...models.dorm import Dorm
from ...models.lunch import Lunch
from ...models.course import Course
from ...utils import SessionMaker, get_time_difference, format_time

class db:

    ELEMENTS = {
        'fire'  : {'aries', 'leo', 'sagittarius'},
        'earth' : {'taurus', 'virgo', 'capricorn'},
        'air'   : {'gemini', 'libra', 'aquarius'},
        'water' : {'cancer', 'scorpio', 'pisces'}
    }

    FIRE_AIR    = ELEMENTS['fire']  | ELEMENTS['air']
    EARTH_WATER = ELEMENTS['earth'] | ELEMENTS['water']

    DISTANCE = {
        'North Quad'    : 'DPAC',
        'West Quad'     : 'Stepan Center',
        'Mod Quad'      : 'Pizza Pi',
        'South Quad'    : 'Jordan Hall',
        'Far Quad'      : 'campus',
        'God Quad'      : 'Pasquerilla Center',
        'East Quad'     : 'The Rock'
    }

    DISPLAY_DAYS = { 'MO' : 'Monday',
                     'TU' : 'Tuesday',
                     'WE' : 'Wednesday',
                     'TH' : 'Thursday',
                     'FR' : 'Friday' }

    DAYS = {'Sunday'    : 0,
            'Monday'    : 1,
            'Tuesday'   : 2,
            'Wednesday' : 3,
            'Thursday'  : 4,
            'Friday'    : 5,
            'Saturday'  : 6 }

    def __init__(self, Session):
        self.Session = Session

    # Find courses in common between two students
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

    # Find open lunch slots between two students
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

        lunches = list(set(lunches))
        lunches = sorted(lunches, key=lambda lunch: self.DAYS[lunch.split()[0]])

        return lunches
    
    # Find if students attend mass regularly 
    def get_mass_attendance(self, student1, student2):

        sm = SessionMaker(self.Session)
        with sm as session:
            s1 = session.query(Preferences)\
                        .filter(Preferences.netid == student1).first()
            s2 = session.query(Preferences)\
                        .filter(Preferences.netid == student2).first()
        
        attendsMass = {'day', 'week'}
        if s1.mass in attendsMass and s2.mass in attendsMass:
            return True

        return False

    # See if overlap is at least an hour long
    def find_lunch_overlap(self, s1, s2):
        start   = max(s1.starttime.time(), s2.starttime.time())
        end     = min(s1.endtime.time(), s2.endtime.time())
        if get_time_difference(end, start) >= 60:
            return '{} - {}'.format(format_time(start), format_time(end))

    # Build messages based on preferences
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
        messages.append('I\'d walk all the way from {} to {} for you'.format(s1Dorm.dorm, self.DISTANCE[s1Dorm.quad]))
        messages.append(self.get_horoscope_mesage(s1Pref.zodiacsign, s2Pref.zodiacsign))

        # Live on same quad
        if s1Dorm.quad == s2Dorm.quad:
            messages.append('{}, best quad!'.format(s1Dorm.quad))
        
        # Has air conditioning
        if s1Dorm.airconditioning == 1 and s2Dorm.airconditioning == 0:
            messages.append('You should come to {}, we have air conditioning :P'.format(s1Dorm.dorm))

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
        if self.check_horoscope(s1.zodiacsign, s2.zodiacsign):
            compatibility += 1
        if s1.idealtemperament == s2.temperament:
            compatibility += 3
        if s1.receiveaffection == s2.giveaffection:
            compatibility += 3
        if s1.idealtrait == s2.trait:
            compatibility += 3

        return round(compatibility / 34, 4) * 100

    # Check horoscope compatibility
    def check_horoscope(self, sign1, sign2):
        signs = {sign1, sign2}
        if signs.issubset(self.FIRE_AIR) or signs.issubset(self.EARTH_WATER):
            return True
        return False

    # Get message based on horoscope
    def get_horoscope_mesage(self, sign1, sign2):

        # If signs are exactly the same
        if sign1 == sign2:
            return 'Two {} signs are better than one.'.format(sign1)

        # If same element
        signs = {sign1, sign2}
        for e, vals in self.ELEMENTS.items():
            if signs.issubset(vals):
                return self.same_element_message(sign1, sign2, e)

        # If different compatible elements
        if self.check_horoscope(sign1, sign2):
            return self.different_element_message(sign1, sign2)

        # If not compatible
        return 'Oh no, {} and {}? This should be interesting'.format(sign2, sign1)

    # Builds message string when zodiac signs from same elements
    def same_element_message(self, sign1, sign2, element):
        return 'Ooohh hey there {}, this {} has been looking for another {} sign :)'.format(sign2, sign1, element)

    # Builds message string when zodiac signs from different elements
    def different_element_message(self, sign1, sign2):
        return '{} + {} = compatible. The stars don\'t lie.'.format(sign2.title(), sign1)
