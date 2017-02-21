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
        '--version',
        help='Display Peek\'s version',
        action='store_true'
    )
    return parser

# globals, due to asciimatics not accepting other params to the screen
log_file_path = ''


def run_viewer_screen(screen):
    pv = PeekViewer(log_file_path=log_file_path, db_path='logs')
    pv.draw_screen(screen=screen)
    # # print layout once
    # for data in pv.get_static_screen_data():
    #     screen.print_at(data[0], data[1], data[2])
    # while True:
    #     # update only the values
    #     for data in pv.get_dynamic_screen_data():
    #         screen.print_at(data[0], data[1], data[2])
    #     ev = screen.get_key()
    #     if ev in (ord('Q'), ord('q')):
    #         return
    #     screen.refresh()


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
            Screen.wrapper(run_viewer_screen)
        else:
            peek_runner = PeekRunner(file_path=log_file_path)
            peek_runner.parse_logs()
    except KeyboardInterrupt:
        sys.exit(0)



