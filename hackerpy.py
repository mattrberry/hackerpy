from hnpy import hnpy
import curses
import time
import webbrowser


class HackerPy(object):
    def __init__(self):
        self.hn = hnpy.HackerNews()

        self.stdscr = curses.initscr()
        curses.noecho()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.height, self.width = self.stdscr.getmaxyx()

        self.ppp = int(self.height / 2)

        self.screen_start()

        self.capture_input()


    def capture_input(self):
        while True:
            c = self.stdscr.getch()
            if c == ord('q'):
                break
            elif c == curses.KEY_RIGHT:
                self.nextPage()
            elif c == curses.KEY_LEFT:
                self.previousPage()
            elif c == ord('t'):
                self.hnpy_get_render(self.hn.getTop)
            elif c == ord('n'):
                self.hnpy_get_render(self.hn.getNew)
            elif c == ord('b'):
                self.hnpy_get_render(self.hn.getBest)
            elif c == ord('a'):
                self.hnpy_get_render(self.hn.getAsk)
            elif c == ord('s'):
                self.hnpy_get_render(self.hn.getShow)
            elif c == ord('j'):
                self.hnpy_get_render(self.hn.getJob)
            else:
                pass

    def screen_start(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "Commands:")
        self.stdscr.addstr(1, 0, "  q           - quit")
        self.stdscr.addstr(2, 0, "  right arrow - next page")
        self.stdscr.addstr(3, 0, "  left arrow  - previous page")
        self.stdscr.addstr(4, 0, "  t           - top")
        self.stdscr.addstr(5, 0, "  n           - new")
        self.stdscr.addstr(6, 0, "  b           - best")
        self.stdscr.addstr(7, 0, "  a           - ask")
        self.stdscr.addstr(8, 0, "  s           - show")
        self.stdscr.addstr(9, 0, "  j           - jobs")

    def screen_loading(self):
        self.stdscr.clear()
        self.stdscr.addstr(0, 0, "loading...")
        self.stdscr.refresh()

    def screen_posts(self):
        self.stdscr.clear()
        for count, item in enumerate(self.loaded_posts):
            if len(item.title) > self.width:
                title = item.title[:self.width - 3] + "..."
            else:
                title = item.title
            self.stdscr.addstr(count * 2, 0, title)
            self.stdscr.addstr(count * 2 + 1, 2, item.infoString(), curses.A_DIM)

        self.stdscr.refresh()

    def hnpy_get_render(self, hnpy_getter):
        self.screen_loading()
        self.item_ids = hnpy_getter()
        self.page = 0
        self.loadPage(self.item_ids)
        self.screen_posts()

    def nextPage(self):
        self.screen_loading()
        self.page = self.page + 1
        self.loadPage(self.item_ids)
        self.screen_posts()

    def previousPage(self):
        if self.page > 0:
            self.screen_loading()
            self.page = self.page - 1
            self.loadPage(self.item_ids)
            self.screen_posts()

    def loadPage(self, toLoad):
        self.loaded_posts = self.hn.load(toLoad, self.ppp, self.ppp * self.page)


if __name__ == "__main__":
    hp = HackerPy()
