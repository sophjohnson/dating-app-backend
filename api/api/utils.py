from datetime import datetime
from pytz import timezone

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
