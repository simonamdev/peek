import pytest

from peek.config_file import ConfigurationFile
from tests.file_paths import test_log_file_path


class TestConfigurationFileInstantiation:
    @pytest.mark.parametrize('file_path', [
        None,
        1,
        2.0,
        '',
        'foobar',
        object,
        (),
        []
    ])
    def test_passing_non_existent_file_throws_exception(self, file_path):
        with pytest.raises(FileNotFoundError):
            ConfigurationFile(file_path=file_path)

    def test_passing_actual_file(self):
        ConfigurationFile(file_path=test_log_file_path)

    def test_getting_file_length(self):
        config_file = ConfigurationFile(file_path=test_log_file_path)
        assert 10 == config_file.length
