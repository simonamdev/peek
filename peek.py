import argparse

import sys

from peek.peek_runner import PeekRunner
from peek.peek_viewer import PeekViewer


def create_peek_args_parser():
    parser = argparse.ArgumentParser(description='Peek')
    parser.add_argument(
        'file_path',
        type=str,
        help='Nginx log file path')
    parser.add_argument(
        '--persist',
        dest='persist',
        help='Run the Peek Runner, which will persist parsed nginx logs to an SQLite database',
        action='store_true')
    parser.add_argument(
        '--view',
        dest='view',
        help='Run the Peek Viewer, which will show statistics from the logs database',
        action='store_true'
    )
    parser.add_argument(
        '--version',
        help='Display Peek\'s version',
        action='store_true'
    )
    return parser


if __name__ == '__main__':
    parser = create_peek_args_parser()
    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(0)
    elif '--version' in sys.argv:
        print(PeekRunner.version)
        sys.exit(0)
    # TODO: Add logging and pass in args debug flag to change level
    args = parser.parse_args()
    try:
        if args.view:
            # TODO: Change from hardcoded logs db path
            peek_viewer = PeekViewer(log_file_path=args.file_path, db_path='logs.db')
            peek_viewer.run()
        else:
            peek_runner = PeekRunner(file_path=args.file_path)
            peek_runner.parse_logs()
    except KeyboardInterrupt:
        sys.exit(0)
