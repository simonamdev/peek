import copy

import pytest

from peek.line import InvalidIpAddressException, Line, InvalidStatusException

# 127.0.0.1 - - [01/Jan/1970:00:00:01] "GET / HTTP/1.1" 200 193 "-" "Python"
line_contents = {
    'ip_address': '127.0.0.1',
    'timestamp':  '[01/Jan/1970:00:00:01]',
    'verb':       'GET',
    'path':       '/',
    'status':     '200',
    'size':       '193',
    'referrer':   '-',
    'user_agent': 'Python'
}


def get_updated_line_contents(updates=None):
    test_contents = copy.deepcopy(line_contents)
    if updates is not None:
        test_contents.update(updates)
    return test_contents


test_line = Line(line_contents=line_contents)


class TestLineInstantiation:
    @pytest.mark.parametrize('expected,actual', [
        ('127.0.0.1', test_line.ip_address),
        ('01/Jan/1970:00:00:01', test_line.timestamp),
        ('GET', test_line.verb),
        ('/', test_line.path),
        (200, test_line.status),
        (193, test_line.byte_count),
        ('-', test_line.referrer),
        ('Python', test_line.user_agent)
    ])
    def test_retrieval(self, expected, actual):
        assert expected == actual


class TestLineExceptions:
    def test_passing_invalid_ip_address_throws_exception(self):
        with pytest.raises(InvalidIpAddressException):
            Line(get_updated_line_contents({'ip_address': 'foobar'}))

    def test_passing_non_parseable_status_throws_exception(self):
        test_contents = copy.deepcopy(line_contents)
        test_contents['status'] = 'foobar'
        with pytest.raises(InvalidStatusException):
            Line(get_updated_line_contents({'status': 'foobar'}))
