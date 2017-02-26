import argparse

import sys

from asciimatics.screen import Screen

from peek.peek_runner import PeekRunner
from peek.peek_viewer import PeekViewer


def create_peek_args_parser():
    parser = argparse.ArgumentParser(description='Peek')
    parser.add_argument(
        dest='log_file_path',
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
        '--view-interval',
        dest='view_interval',
        type=int,
        help='The interval in seconds that the viewer will query the database. Default is 3'
    )
    parser.add_argument(
        '--version',
        help='Display Peek\'s version',
        action='store_true'
    )
    return parser

# globals, due to asciimatics not accepting other params to the screen
log_file_path = ''
refresh_rate = 3


def run_viewer_screen(screen):
    pv = PeekViewer(log_file_path=log_file_path, db_path='logs', refresh_rate=refresh_rate)
    pv.draw_screen(screen=screen)


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
    log_file_path = args.log_file_path
    try:
        if args.view:
            # TODO: Change from hardcoded logs db path
            if args.view_interval:
                refresh_rate = args.view_interval
            Screen.wrapper(run_viewer_screen)
        else:
            peek_runner = PeekRunner(file_path=log_file_path)
            peek_runner.parse_logs()
    except KeyboardInterrupt:
        sys.exit(0)



