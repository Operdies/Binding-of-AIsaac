"""
Special thanks to Lithian Coth on Stack Overflow for
reading the documentation so I didn't have to
"""
import win32gui
import win32con
import win32api
from time import sleep
import random


class Game(object):

    actionDict = {
        'A':         ord('A'),
        'S':         ord('S'),
        'W':         ord('W'),
        'D':         ord('D'),
        'Q':         ord('Q'),
        'E':         ord('E'),
        ' ':         ord(' '),
        'UA':        win32con.VK_UP,
        'DA':        win32con.VK_DOWN,
        'LA':        win32con.VK_LEFT,
        'RA':        win32con.VK_RIGHT,
        'CTRL':      win32con.VK_CONTROL,
        'CTRL_DROP': -1,
    }

    actions = [ord('A'),
               ord('S'),
               ord('W'),
               ord('D'),
               ord('Q'),
               ord('E'),
               ord(' '),
               win32con.VK_UP,
               win32con.VK_DOWN,
               win32con.VK_LEFT,
               win32con.VK_RIGHT,
               win32con.VK_CONTROL,
               ]

    oldActions = [0] * len(actions)

    def __init__(self, ScoreReader, title='Binding'):
        self.title = title
        self.hwnd = 0
        self.getScore = ScoreReader.getScore
        self.counter = 0
        self.score = self.getScore()
        self.forceContinues = 0
        self.sleeptime = 0.033333  # 30 aps - for now
        win32gui.EnumWindows(self.enumHandler, None)

    def enumHandler(self, hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            if self.title in win32gui.GetWindowText(hwnd):
                self.hwnd = hwnd
                print('Found: ', win32gui.GetWindowText(hwnd))

    def send(self, currentActions, countermeasures=False):
        if countermeasures:
            self.counter = self.counter + 1
            if self.counter % 150 == 0:
                if self.score == self.getScore():
                    self.forceContinue()

        for i in range(0, len(self.actions)):
            if not currentActions[i] and self.oldActions[i]:
                win32api.PostMessage(
                    self.hwnd, win32con.WM_KEYUP, self.actions[i], 0)
            if currentActions[i]:
                win32api.PostMessage(
                    self.hwnd, win32con.WM_KEYDOWN, self.actions[i], 0)

        self.oldActions = currentActions[:]
        sleep(self.sleeptime)  # Remove later I guessnum

    def forceContinue(self):
        # print("This guy.. thought he could trick me.")
        self.forceContinues += 1
        # key = self.actionDict[' ']
        key = win32con.VK_RETURN
        win32api.PostMessage(self.hwnd, win32con.WM_KEYDOWN, key, 0)
        sleep(0.1)
        win32api.PostMessage(self.hwnd, win32con.WM_KEYUP, key, 0)
