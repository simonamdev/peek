from peek.log_statistics import LogStatistics


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

    #
    # def test_inserting_logs(self):
    #     pass
