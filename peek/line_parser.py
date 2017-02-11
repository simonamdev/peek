class LineParser:
    @staticmethod
    def __validate(line):
        if not isinstance(line, str):
            raise ValueError('Line must be a string')

    @staticmethod
    def parse_line(line):
        LineParser.__validate(line=line)
