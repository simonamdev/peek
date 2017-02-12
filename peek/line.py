import re


class Line:
    def __init__(self, row):
        self._ip_address = row[0]
        self._timestamp = row[1].replace('[', '').replace(']', '')
        self._verb = row[2]
        self._path = row[3]
        self._status = row[4]
        self._byte_count = row[5]
        self._referrer = row[6]
        self._user_agent = row[7]
        self.__validate()

    def __validate(self):
        ip_pattern = '\\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                     '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                     '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                     '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b'
        match = re.findall(ip_pattern, self._ip_address)
        if len(match) == 0:
            raise InvalidIpAddressException
        try:
            int(self._status)
        except ValueError:
            raise InvalidStatusException

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


class InvalidIpAddressException(ValueError):
    pass


class InvalidStatusException(ValueError):
    pass
