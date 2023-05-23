import curses
from model import Object
from typing import List

stdscr = curses.initscr()

class View:
    game_window = None
    bar_window = None

    @classmethod
    def is_window_big_enough(cls, rows, cols):
        try:
            terminal_rows, terminal_cols = stdscr.getmaxyx()
            if terminal_rows >= rows and terminal_cols >= cols:
                return True
            else:
                return False
        finally:
            curses.endwin()

    @classmethod
    def start_session(cls, rows, cols):
        stdscr.clear()
        curses.cbreak()
        stdscr.keypad(True)
        curses.noecho()
        curses.curs_set(0)
        curses.start_color()
        terminal_height, terminal_width = stdscr.getmaxyx()

        cls.print_centered("WARNING: PHOTOSENSITIVITY/EPILEPSY SEIZURES")

        window_y = (terminal_height - rows) // 2  
        window_x = (terminal_width - cols) // 2

        cls.game_window = curses.newwin(rows, cols, window_y, window_x)
        cls.bar_window = curses.newwin(3, cols, window_y - 3, window_x)


    @classmethod
    def draw(cls, objects: List[Object], highscore, health):
        curses.init_pair(1, curses.COLOR_WHITE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_RED, curses.COLOR_BLACK)
        cls.game_window.clear()
        cls.bar_window.clear()
        cls.game_window.box()
        cls.bar_window.box()
        for obj in objects:
            cls.game_window.addstr(obj.y + 1, obj.x + 1, obj.body, curses.color_pair(obj.color) | curses.A_BOLD)
        cls.bar_window.addstr(1, 1, f'Highscore: {highscore}', curses.A_BOLD)
        cls.bar_window.addstr(1, 33, 'Health: ', curses.A_BOLD)
        cls.bar_window.addstr(1, 40, health * " <3", curses.color_pair(4) | curses.A_BOLD)
        cls.game_window.refresh()
        cls.bar_window.refresh()

    @classmethod
    def win(cls, score):
        cls.print_centered(f'YOU WON WITH SCORE {score}')

    @classmethod
    def lose(cls, score):
        cls.print_centered(f'YOU LOST WITH SCORE {score}')

    @classmethod
    def print_centered(cls, text):
        stdscr.clear()
        rows, columns = stdscr.getmaxyx()
        x = columns // 2 - len(text) // 2
        y = rows // 2
        stdscr.addstr(y, x, text, curses.A_BOLD)
        stdscr.refresh()
        stdscr.getch()

    @classmethod
    def end_session(cls):
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()