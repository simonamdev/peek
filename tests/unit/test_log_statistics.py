from peek.log_statistics import LogStatistics


class TestLogStatisticsInstantiation:
    def test_starting_without_persistence(self):
        log_statistics = LogStatistics()
        assert False is log_statistics.persistence_mode

    def test_starting_with_persistence(self):
        log_statistics = LogStatistics(persist=True)
        assert True is log_statistics.persistence_mode
