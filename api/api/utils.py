from datetime import datetime, date
from pytz import timezone

class CORSComponent(object):
    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', '*')

        if (req_succeeded
            and req.method == 'OPTIONS'
            and req.get_header('Access-Control-Request-Method')
        ):

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers',
                default='*'
            )

            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', '86400'),  # 24 hours
            ))

# Session maker context manager
class SessionMaker():

    def __init__(self, sm):
        self.session = sm()

    def __enter__(self):
        return self.session

    def __exit__(self, type, value, traceback):
        self.session.close()

# Functions for timestamp formatting
class TimeWindow():
    def __init__(self, start, end):
        self.start = start
        self.end = end

def format_datetime(ts):
    return ts.strftime("%m/%d/%y, %I:%M %p")

def format_time(ts):
    ts = datetime.combine(date.today(), ts)
    return ts.strftime("%I:%M %p")

# Get current time
def get_curr_time():
    return datetime.now().astimezone(timezone('US/Eastern'))

# Get earliest representable datetime (for comparison)
def get_earliest_time():
    return datetime.min

# Get difference between two time objects
def get_time_difference(date1, date2):
    date1 = datetime.combine(date.today(), date1)
    date2 = datetime.combine(date.today(), date2)
    return (date1 - date2).seconds // 60
