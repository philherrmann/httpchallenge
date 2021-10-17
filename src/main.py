from threading import Thread
from src.controllers.controller import Controller

import time


from src.views.print_view import PrintView
from src.views.curses_view import CursesView


def main():
    #controller = Controller(view=PrintView())
    controller = Controller(view=CursesView())
    print("start controller")
    #put it in a thread
    # or send an event on keystroke
    #controller_thread = Thread()
    #controller_thread.start()
    controller.start()
    time.sleep(30)
    print("end controller")
    controller.stop()


if __name__ == '__main__':
    main()
