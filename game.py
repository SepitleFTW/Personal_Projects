import curses
from curses import wrapper
import time
import random

def start_screen(stdscre):
    stdscre.clear()
    stdscr.addstr("Welcome to the Speed Type Test!")
    stdscr.addstr("\nPress any key to continue")
    stdscr.refresh()
    stdscr.getkey()

def display_text(stdscr, target, current, wpm=0):
    stdscr.addstr(target)
    stdscr.addstr(1, 0. f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
