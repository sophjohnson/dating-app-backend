from icalendar import Calendar
from datetime import datetime, date, time

from ...models.student import Student
from ...models.course import Course
from ...utils import SessionMaker

class db:

    def __init__(self, Session):
        self.Session = Session

    # Parse .ics file
    def parse_schedule(self, req, netid):

        courses = self.parse_courses(req)
        self.create_courses(netid, courses)
        return courses

    # Get list of courses student is in
    def parse_courses(self, req):
        cal = Calendar.from_ical(req.stream.read())

        courses = [ self.parse_course(event) for event in cal.walk('vevent')]
        return courses

    # Get information for one course
    def parse_course(self, event):

        summary = str(event['SUMMARY']).split()
        course = { 'name'     : ' '.join(summary[:-3]),
                   'course'   : ' '.join(summary[-3:-1]),
                   'section'  : summary[-1] }

        return course

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
