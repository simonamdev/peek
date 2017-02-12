import time

from tests.file_paths import real_log_file_path


def watch_file(file_path):
    with open(file_path, 'r') as log_file:
        # Go to the end of the file
        log_file.seek(0, 2)
        line = log_file.readline()
        if line:
            yield line
        time.sleep(1)


if __name__ == '__main__':
    for incoming_line in watch_file(real_log_file_path):
        print(incoming_line)
