from icalendar import Calendar
from datetime import datetime, date, time

from ...models.student import Student
from ...models.course import Course
from ...models.lunch import Lunch
from ...utils import SessionMaker, TimeWindow, get_time_difference, to_datetime, format_time
from falcon import HTTPBadRequest

class db:

    DAYS = ['MO', 'TU', 'WE', 'TH', 'FR']

    LUNCH_START     = time(11, 00)
    LUNCH_END       = time(14, 00)
    LUNCH_DURATION  = 60

    def __init__(self, Session):
        self.Session = Session

    # Parse .ics file
    def parse_schedule(self, req, netid):
        cal = Calendar.from_ical(req.stream.read())
        result = {}

        # Parse courses
        result['courses'] = self.parse_all_courses(cal)
        self.create_courses(netid, result['courses'])

        # Parse lunches
        lunches = self.parse_all_lunches(cal)
        self.create_lunches(netid, lunches)
        result['lunches'] = self.format_lunches(lunches)

        return result

    # Get list of courses student is in
    def parse_all_courses(self, cal):
        courses = [ self.parse_course(event) for event in cal.walk('vevent')]
        return courses

    # Get information for one course
    def parse_course(self, event):

        summary = str(event['SUMMARY']).split()
        course = { 'name'     : ' '.join(summary[:-3]),
                   'course'   : ' '.join(summary[-3:-1]),
                   'section'  : summary[-1] }

        return course

    # Create courses and record student/course relationship
    def create_courses(self, netid, courses):

        sm = SessionMaker(self.Session)
        with sm as session:

            # Get student
            student = session.query(Student).filter(Student.netid == netid).scalar()

            # If student doesn't exist
            if student is None:
                msg = "No student exists for given netid."
                raise HTTPBadRequest("Bad Request", msg)

            # Remove existing courses
            student.courses.clear()
            session.commit()

            # Record new course
            studentCourses = []
            for c in courses:
                course = session.query(Course).filter(Course.id == c['course']).scalar()

                # Add course if necessary
                if course is None:
                    course = Course(
                        id      = c['course'],
                        course  = c['name']
                    )
                    session.add(course)
                    session.commit()

                studentCourses.append(course)

            student.courses = studentCourses
            session.commit()

    def parse_all_lunches(self, cal):
        busy = {d: [] for d in self.DAYS}

        for event in cal.walk('vevent'):

            # Parse start and end times
            start   = event['DTSTART'].dt.time()
            end     = event['DTEND'].dt.time()

            # Record time windows that overlap with lunch
            if end > self.LUNCH_START and start < self.LUNCH_END:
                days = event['RRULE']['BYDAY']
                for day in days:
                    busy[day].append(TimeWindow(start, end))

        lunchBreaks = { day: self.parse_lunches(times) for day, times in busy.items() }

        return lunchBreaks

    def format_lunches(self, lunchBreaks):
        lunchBreaks = { day : [ { 'start' : format_time(b.start),
                                  'end' : format_time(b.end) } for b in breaks ] for day, breaks in lunchBreaks.items() }
        return lunchBreaks

    # Get lunch breaks given busy segments of one day
    def parse_lunches(self, times):

        windows = [ TimeWindow(self.LUNCH_START, self.LUNCH_END) ]

        for time in times:
            # Overlaps beginning of lunch
            if time.start <= windows[0].start:
                windows[0].start = time.end
            # Overlaps end of lunch
            elif time.end >= windows[-1].end:
                windows[-1].end = time.start
            # Inside lunch break, split time window into two
            else:
                splitWindows = []
                for i, window in enumerate(windows):
                    if time.start >= window.start and time.end <= window.end:
                        splitWindows.append(TimeWindow(window.start, time.start))
                        splitWindows.append(TimeWindow(time.end, window.end))
                    else:
                        splitWindows.append(window)
                windows = splitWindows

        # Find lunch breaks longer than provided duration
        windows = [ w for w in windows if get_time_difference(w.end, w.start) >= self.LUNCH_DURATION ]

        return windows

    # Create lunches
    def create_lunches(self, netid, lunchBreaks):

        sm = SessionMaker(self.Session)
        with sm as session:

            # Delete current lunches
            student = session.query(Lunch).filter(Lunch.netid == netid).delete()
            session.commit()

            # Record new lunches
            for day, breaks in lunchBreaks.items():
                for b in breaks:

                    lunch = Lunch(
                        netid       = netid,
                        day         = day,
                        starttime   = to_datetime(b.start),
                        endtime     = to_datetime(b.end)
                    )
                    session.add(lunch)
                    session.commit()
