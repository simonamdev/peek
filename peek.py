import argparse

import sys

from peek.peek_runner import PeekRunner


def create_peek_args_parser():
    parser = argparse.ArgumentParser(
        description='Peek')
    parser.add_argument(
        'file_path',
        type=str,
        help='Nginx log file path')
    parser.add_argument(
        '--persist',
        dest='persist',
        help='Persist parsed nginx logs to an SQLite database',
        action='store_true')
    return parser


if __name__ == '__main__':
    args = create_peek_args_parser().parse_args()
    # TODO: Add logging and pass in args debug flag to change level
    peek_runner = PeekRunner(file_path=args.file_path, persist=args.persist)
    try:
        peek_runner.parse_logs()
    except KeyboardInterrupt:
        sys.exit(0)
