import pytest

from peek.log_file import LogFile
from tests.file_paths import test_log_file_path


class TestLogFileInstantiation:
    @pytest.mark.parametrize('file_path', [
        '',
        'foobar'
    ])
    def test_passing_non_existent_file_throws_exception(self, file_path):
        with pytest.raises(FileNotFoundError):
            LogFile(file_path=file_path)

    @pytest.mark.parametrize('file_path', [
        1,
        None,
        2.0,
        object,
        (),
        []
    ])
    def test_passing_incorrect_params_throws_exception(self, file_path):
        with pytest.raises(TypeError):
            LogFile(file_path=file_path)

    def test_passing_actual_file(self):
        LogFile(file_path=test_log_file_path)

    def test_getting_file_path(self):
        config_file = LogFile(file_path=test_log_file_path)
        assert test_log_file_path == config_file.file_path

    def test_getting_file_length(self):
        config_file = LogFile(file_path=test_log_file_path)
        assert 10 == config_file.length
