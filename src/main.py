import os
import sys

path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

print(f"SYSPATH {sys.path}")

import argparse
import time
from threading import Thread
from src.controllers.controller import Controller


from interfaces.abstract_view import AbstractView
from src.views.print_view import PrintView
from src.views.curses_view import CursesView


class ControllerThread(Thread):

    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller

    def run(self):
        self.controller.start()


def main(selected_view: AbstractView):
    # update period: 10 seconds
    # traffic history for alerting: 2 minutes / 120 seconds
    # traffic limit: 10k bytes (which is low)
    controller = Controller(view=selected_view,
                            update_period=10,
                            traffic_history_span=120,
                            traffic_limit=10000)
    print("start controller")
    controller_thread = ControllerThread(controller)
    controller_thread.start()
    '''
    # in principle application should run 'forever'
    time.sleep(3000)
    controller.stop()
    controller_thread.join()
    '''


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Console scroll or curses.')
    parser.add_argument('--ncurses', default=False, dest='ncurses', action='store_true',
                        help='ncurses mode (default: scrolling)')
    args = vars(parser.parse_args())
    if "ncurses" in args and args["ncurses"]:
        view = CursesView()
    else:
        view = PrintView()
    main(view)
