# Session maker context manager
class SessionMaker():

    def __init__(self, sm):
        self.session = sm()

    def __enter__(self):
        return self.session

    def __exit__(self, type, value, traceback):
        self.session.close()
