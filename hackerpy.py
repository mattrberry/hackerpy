from hnpy import hnpy
import curses
import time
import webbrowser


class HackerPy(object):
    def __init__(self):
        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.height, self.width = self.stdscr.getmaxyx()

        self.ppp = int((self.height - 1) / 2)

        self.screen_loading()

        self.hn = hnpy.HackerNews()
        self.hn.getTop()
        self.page = 0
        self.loadPage()
        self.screen_posts()

        self.stdscr.getkey()

    def screen_loading(self):
        self.stdscr.clear()
        self.stdscr.addstr(1, 1, "loading...")
        self.stdscr.refresh()

    def screen_posts(self):
        self.stdscr.clear()
        for count, item in enumerate(self.hn.loaded):
            if len(item.title) > self.width:
                title = item.title[:self.width - 3] + "..."
            else:
                title = item.title
            self.stdscr.addstr(count * 2, 0, title)
            self.stdscr.addstr(count * 2 + 1, 2, item.infoString(), curses.A_DIM)
        self.stdscr.refresh()

    def nextPage(self):
        self.page = self.page + 1
        self.loadPage()
        self.screen_posts()

    def loadPage(self):
        self.hn.load(self.hn.top, self.ppp, self.ppp * self.page)


if __name__ == "__main__":
    hp = HackerPy()
