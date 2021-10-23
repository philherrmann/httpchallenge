import os
import sys

path = os.path.join(os.path.dirname(__file__), os.pardir)
sys.path.append(path)

from threading import Thread
from src.controllers.controller import Controller

import time


from src.views.print_view import PrintView
from src.views.curses_view import CursesView


class ControllerThread(Thread):

    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = controller

    def run(self):
        self.controller.start()


def main():
    #controller = Controller(view=CursesView())
    controller = Controller(view=PrintView(), update_period=2, traffic_history_span=20)
    print("start controller")
    controller_thread = ControllerThread(controller)
    controller_thread.start()
    time.sleep(3000)
    print("end controller")
    controller.stop()
    print("join controller")
    controller_thread.join()


if __name__ == '__main__':
    main()
