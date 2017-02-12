from peek.line import Line
from peek.line_parser import LineParser
from peek.log_statistics import LogStatistics
from tests.unit.test_line import get_updated_line_contents

test_string_one = '127.0.0.1 - - [01/Jan/1970:00:00:01] "GET / HTTP/1.1" 200 150 "-" "Python"'
test_string_two = '127.0.0.2 - - [01/Jan/1970:00:00:01] "POST /api/ HTTP/1.1" 201 350 "ref" "Ruby"'


class TestLogStatisticsInstantiation:
    def test_starting_without_persistence(self):
        log_statistics = LogStatistics()
        assert False is log_statistics.persistence_mode

    def test_starting_with_persistence(self):
        log_statistics = LogStatistics(persist=True)
        assert True is log_statistics.persistence_mode


class TestLogStatistics:
    def test_new_non_persistent_line_count_is_0(self):
        log_statistics = LogStatistics()
        assert 0 == log_statistics.lines_stored

    def test_new_non_persistent_retrieval_is_empty(self):
        log_statistics = LogStatistics()
        assert [] == log_statistics.get_all_lines()

    def test_inserting_and_retrieving_logs(self):
        line_contents = get_updated_line_contents()
        log_statistics = LogStatistics()
        test_line = Line(line_contents=line_contents)
        log_statistics.insert_line(line=test_line)
        assert 1 == log_statistics.lines_stored
        lines = log_statistics.get_all_lines()
        assert lines[0].ip_address == test_line.ip_address
        assert lines[0].timestamp == test_line.timestamp
        assert lines[0].verb == test_line.verb
        assert lines[0].path == test_line.path
        assert lines[0].status == test_line.status
        assert lines[0].byte_count == test_line.byte_count
        assert lines[0].referrer == test_line.referrer
        assert lines[0].user_agent == test_line.user_agent

    def test_inserting_none_has_no_effect(self):
        log_statistics = LogStatistics()
        assert 0 == log_statistics.lines_stored
        log_statistics.insert_line(line=None)
        assert 0 == log_statistics.lines_stored

    def test_retrieving_number_of_ip_occurrences(self):
        log_statistics = LogStatistics()
        for i in range(0, 10):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_one))
        for i in range(0, 5):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_two))
        ip_address_occurrences = log_statistics.get_ip_address_occurrences()
        assert 10 == ip_address_occurrences['127.0.0.1']
        assert 5 == ip_address_occurrences['127.0.0.2']

    def test_retrieving_number_of_distinct_ip_addresses(self):
        log_statistics = LogStatistics()
        log_statistics.insert_line(line=LineParser.parse_line(line=test_string_one))
        log_statistics.insert_line(line=LineParser.parse_line(line=test_string_two))
        assert 2 == log_statistics.get_number_of_distinct_ip_addresses()

    def test_retrieving_number_of_verb_occurrences(self):
        log_statistics = LogStatistics()
        for i in range(0, 2):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_one))
        for i in range(0, 4):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_two))
        verb_occurrences = log_statistics.get_verb_occurrences()
        assert 2 == verb_occurrences['GET']
        assert 4 == verb_occurrences['POST']

    def test_retrieving_number_of_path_occurrences(self):
        log_statistics = LogStatistics()
        for i in range(0, 4):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_one))
        for i in range(0, 2):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_two))
        path_occurrences = log_statistics.get_path_occurrences()
        assert 4 == path_occurrences['/']
        assert 2 == path_occurrences['/api/']

    def test_retrieving_status_occurrences(self):
        log_statistics = LogStatistics()
        for i in range(0, 3):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_one))
        for i in range(0, 2):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_two))
        status_occurrences = log_statistics.get_status_occurrences()
        assert 3 == status_occurrences[200]
        assert 2 == status_occurrences[201]

    def test_retrieving_byte_count_average(self):
        log_statistics = LogStatistics()
        for i in range(0, 3):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_one))
        for i in range(0, 3):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_two))
        assert 250.0 == log_statistics.get_average_byte_count()

    def test_retrieving_byte_count_total(self):
        log_statistics = LogStatistics()
        for i in range(0, 3):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_one))
        for i in range(0, 3):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_two))
        assert 1500.0 == log_statistics.get_total_byte_count()

    def test_retrieving_referrer_occurrences(self):
        log_statistics = LogStatistics()
        for i in range(0, 1):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_one))
        for i in range(0, 2):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_two))
        referrer_occurrences = log_statistics.get_referrer_occurrences()
        assert 1 == referrer_occurrences['-']
        assert 2 == referrer_occurrences['ref']

    def test_retrieving_user_agent_occurrences(self):
        log_statistics = LogStatistics()
        for i in range(0, 2):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_one))
        for i in range(0, 2):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_two))
        user_agent_occurrences = log_statistics.get_user_agent_occurrences()
        assert 2 == user_agent_occurrences['Python']
        assert 2 == user_agent_occurrences['Ruby']
