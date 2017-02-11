class Line:
    def __init__(self, row):
        self._ip_address = row[0]
        self._timestamp = row[1]
        self._verb = row[2]
        self._path = row[3]
        self._byte_count = row[4]
        self._referrer = row[5]
        self._user_agent = row[6]
