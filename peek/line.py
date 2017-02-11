class Line:
    def __init__(self, row):
        self._ip_address = row[0]
        self._timestamp = row[1]
        self._verb = row[2]
        self._path = row[3]
        self._status = row[4]
        self._byte_count = row[5]
        self._referrer = row[6]
        self._user_agent = row[7]

    @property
    def ip_address(self):
        return self._ip_address

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def verb(self):
        return self._verb

    @property
    def path(self):
        return self._path

    @property
    def status(self):
        return int(self._status)

    @property
    def byte_count(self):
        return int(self._byte_count)

    @property
    def referrer(self):
        return self._referrer

    @property
    def user_agent(self):
        return self._user_agent
