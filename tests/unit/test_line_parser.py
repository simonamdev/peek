import pytest

from peek.line import Line
from peek.line_parser import LineParser


class TestLineParser:
    @pytest.mark.parametrize('line', [
        None,
        1,
        object,
        (),
        [],
        {}
    ])
    def test_passing_incorrect_parameters_throws_exception(self, line):
        with pytest.raises(ValueError):
            LineParser.parse_line(line=line)

    def test_passing_empty_line_returns_none(self):
        assert None is LineParser.parse_line(line='')

    def test_passing_non_matching_line_returns_none(self):
        assert None is LineParser.parse_line('blablablabla')

    def test_passing_valid_line_returns_line(self):
        line = LineParser.parse_line('127.0.0.1 - - [01/Jan/1970:00:00:01] "GET / HTTP/1.1" 200 193 "-" "Python"')
        assert isinstance(line, Line)
