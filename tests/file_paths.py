import os

current_directory = os.path.dirname(os.path.realpath(__file__))
test_file_directory = os.path.join(current_directory, 'files')
test_log_file_path = os.path.join(test_file_directory, 'test.txt')
watch_test_log_file_path = os.path.join(test_file_directory, 'watch_test.txt')
real_log_file_path = os.path.join(test_file_directory, 'real_access.log')
