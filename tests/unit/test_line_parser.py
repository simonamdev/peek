import pytest

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
