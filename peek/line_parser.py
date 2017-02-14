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
               '(\d+)\s'                        # size
               '"(.+)"\s'                       # referrer
               '"(.+)"'                         # useragent
               )
        match = re.findall(pat, line)
        if not match:
            return None
        line_contents = {
            'ip_address': match[0][0],
            'timestamp':  match[0][1],
            'verb':       match[0][2],
            'path':       match[0][3],
            'status':     match[0][4],
            'size':       match[0][5],
            'referrer':   match[0][6],
            'user_agent': match[0][7]
        }
        return Line(line_contents=line_contents)
