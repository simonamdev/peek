import datetime
import re


class Line:
    def __init__(self, line_contents):
        self._line_contents = line_contents
        self.__validate()

    def __validate(self):
        ip_pattern = '\\b(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                     '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                     '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.' \
                     '(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\b'
        match = re.findall(ip_pattern, self.ip_address)
        if len(match) == 0:
            raise InvalidIpAddressException
        try:
            int(self.status)
        except ValueError:
            raise InvalidStatusException
        self.__convert_timestamp()

    def __convert_timestamp(self):
        if isinstance(self._line_contents['timestamp'], int):
            return
        # Convert the timestamp
        timestamp_format = '%d/%b/%Y:%H:%M:%S %z'
        if '[' in self._line_contents['timestamp']:
            timestamp_format = '[' + timestamp_format + ']'
        self._line_contents['timestamp'] = int(
            datetime.datetime.strptime(self._line_contents['timestamp'], timestamp_format).timestamp())

    @property
    def ip_address(self):
        return self._line_contents['ip_address']

    @property
    def timestamp(self):
        return self._line_contents['timestamp']

    @property
    def verb(self):
        return self._line_contents['verb']

    @property
    def path(self):
        return self._line_contents['path']

    @property
    def status(self):
        return int(self._line_contents['status'])

    @property
    def byte_count(self):
        return int(self._line_contents['size'])

    @property
    def referrer(self):
        return self._line_contents['referrer']

    @property
    def user_agent(self):
        return self._line_contents['user_agent']


class InvalidIpAddressException(ValueError):
    pass


class InvalidStatusException(ValueError):
    pass
