from peek.line_parser import LineParser
from peek.log_statistics import LogStatistics

test_string_one = '127.0.0.1 - - [01/Jan/1970:00:00:01 +0000] "GET / HTTP/1.1" 200 150 "-" "Python"'
test_string_two = '127.0.0.2 - - [01/Jan/1970:00:00:02 +0000] "POST /api/ HTTP/1.1" 201 350 "ref" "Ruby"'
test_string_three = '127.0.0.2 - - [01/Jan/1970:00:00:03 +0000] "POST /api/ HTTP/1.1" 201 350 "ref" "Ruby"'


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
        log_statistics = LogStatistics()
        test_line = LineParser.parse_line(line=test_string_one)
        log_statistics.insert_line(line=test_line)
        assert 1 == log_statistics.lines_stored
        lines = log_statistics.get_all_lines()
        assert test_line.ip_address == lines[0].ip_address
        assert 1 == lines[0].timestamp
        assert test_line.verb == lines[0].verb
        assert test_line.path == lines[0].path
        assert test_line.status == lines[0].status
        assert test_line.byte_count == lines[0].byte_count
        assert test_line.referrer == lines[0].referrer
        assert test_line.user_agent == lines[0].user_agent

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
        log_statistics.insert_line(line=LineParser.parse_line(line=test_string_one))
        log_statistics.insert_line(line=LineParser.parse_line(line=test_string_two))
        log_statistics.insert_line(line=LineParser.parse_line(line=test_string_two))
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

    def test_get_requests_per_second(self):
        log_statistics = LogStatistics()
        for i in range(0, 5):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_two))
        for i in range(0, 5):
            log_statistics.insert_line(line=LineParser.parse_line(line=test_string_three))
        assert 0.167 == log_statistics.get_requests_per_second_in_timestamp(
            timespan_start=2,
            timespan_end=3)
