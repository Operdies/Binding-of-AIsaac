import win32gui
import win32con
import win32ui
import numpy as np
from timeit import default_timer as timer
import _thread
from PIL import Image
from time import sleep


# noinspection PyAttributeOutsideInit
class Eye(object):

    def __init__(self, title):
        self.RGBCoefficients = np.asarray([0.299, 0.587, 0.114])
        self.title = title
        win32gui.EnumWindows(self.enumHandler, None)
        self.getDimensions()
        hDesktop = win32gui.GetDesktopWindow()
        hDesktopDC = win32gui.GetWindowDC(hDesktop)
        self.hSrcDC = win32ui.CreateDCFromHandle(hDesktopDC)
        self.hMemDC = self.hSrcDC.CreateCompatibleDC()
        self.hBitmap = win32ui.CreateBitmap()
        self.hBitmap.CreateCompatibleBitmap(
            self.hSrcDC, self.cWidth, self.cHeight)
        self.hMemDC.SelectObject(self.hBitmap)
        self.alive = True
        self.autoUpdate()

    def __del__(self):
        self.alive = False

    def getDimensions(self):
        left, top, right, bot = win32gui.GetWindowRect(self.hGame)
        left += 40
        top += 50
        right -= 40
        bot -= 100
        self.left = left
        self.top = top
        self.width = right - left
        self.height = bot - top
        self.cWidth = self.width // 4
        self.cHeight = self.height // 4  # 4*4 = 16x Compression

    def updateBitmap(self):
        # self.getDimensions()
        while self.alive:
            self.hMemDC.StretchBlt((0, 0), (self.cWidth, self.cHeight), self.hSrcDC, (
                self.left, self.top), (self.width, self.height), win32con.SRCCOPY)
            _thread.start_new_thread(self.updateVector, ())

        # self.hMemDC.BitBlt((0, 0), (self.width, self.height), self.hSrcDC,
        # (self.left, self.top), win32con.SRCCOPY) # - exact copy

    def updateVector(self):
        image = self.hBitmap.GetBitmapBits()
        # Get a pixel vector from the bitmap and produce a matrix. Then drop the alpha-channel column
        vector = np.reshape(image, (-1, 4))[:, :3]
        # Scale RGB values by coefficients
        vector = self.RGBCoefficients * vector
        # Sum scaled RGB values and produce an intensity value vector
        self.vector = vector.sum(axis=1)

    def enumHandler(self, hGame, lParam):
        if win32gui.IsWindowVisible(hGame):
            if self.title in win32gui.GetWindowText(hGame):
                self.hGame = hGame
                print('Found: ', win32gui.GetWindowText(hGame))

    def autoUpdate(self):
        _thread.start_new_thread(self.updateBitmap, ())

    def savegs(self, title='gs.gif'):
        gs = self.vector.astype(np.uint8)
        gs = gs.reshape((self.cHeight, self.cWidth))
        img = Image.fromarray(gs, 'L')
        img.save(title)


if __name__ == '__main__':
    eye = Eye('Binding')
    sleep(10)




"""
def savebm(eye):
    # bm = eye.getCompressedBitmap()
    # bm.SaveBitmapFile(eye.hMemDC, 'p.bmp')
    eye.hBitmap.SaveBitmapFile(eye.hMemDC, 'pc.bmp')

eye = Eye('Binding')
def bench(eye):
    start = timer()
    eye.updateBitmap()
    # print('elapsed', timer() - start)
    return timer() - start

def report(res):
    print(res.mean())
    print(res.min())
    print(res.max())

res = np.zeros(500)

for i in range(0,500):
    res[i] = bench(eye)

report(res)
"""
