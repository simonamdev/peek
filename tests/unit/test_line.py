import pytest

from peek.line_parser import LineParser


test_line = LineParser.parse_line(line='127.0.0.1 - - [01/Jan/1970:00:00:01] "GET / HTTP/1.1" 200 193 "-" "Python"')
# 127.0.0.1 - - [01/Jan/1970:00:00:01] "GET / HTTP/1.1" 200 193 "-" "Python"


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
    def test_passing_invalid_url_throws_exception(self):
        assert False is True

