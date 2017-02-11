import re

from peek.line import Line


class LineParser:
    @staticmethod
    def __validate(line):
        if not isinstance(line, str):
            raise ValueError('Line must be a string')

    @staticmethod
    def parse_line(line):
        LineParser.__validate(line=line)
        pat = (r''
               '(\d+.\d+.\d+.\d+)\s-\s-\s'      # IP address
               '\[(.+)\]\s'                     # datetime
               '"(GET|POST)\s'                  # verb
               '(.+)\s\w+/.+"\s'                # path
               '(\d+)\s'                        # status
               '(\d+)\s'                        # bytes sent
               '"(.+)"\s'                       # referrer
               '"(.+)"'                         # useragent
               )
        match = re.findall(pat, line)
        if not match:
            return None
        return Line(match[0])
