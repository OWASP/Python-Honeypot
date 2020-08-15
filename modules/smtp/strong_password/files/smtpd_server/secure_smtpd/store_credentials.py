class StoreCredentials(object):
    def __init__(self):
        self.stored = False
        self.username = None
        self.password = None

    def validate(self, username, password):
        self.stored = True
        self.username = username
        self.password = password
        return True
