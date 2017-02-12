import pytest

from peek.line import Line
from peek.line_parser import LineParser
from tests.unit.test_log_statistics import test_string_one


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
        line = LineParser.parse_line(test_string_one)
        assert isinstance(line, Line)
