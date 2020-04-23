from datetime import datetime
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
def format_time(ts):
    return ts.strftime("%m/%d/%y, %I:%M %p")

def get_curr_time():
    return datetime.now().astimezone(timezone('US/Eastern'))
