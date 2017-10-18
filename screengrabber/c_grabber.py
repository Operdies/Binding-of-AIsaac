import ctypes
import os
from PIL import Image

LibName = 'prtscn.so'
AbsLibPath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep + LibName
grab = ctypes.CDLL(AbsLibPath)


def grab_screen(x1, y1, x2, y2):
    w, h = x1 + x2, y1 + y2
    size = w * h
    objlength = size * 3

    grab.getScreen.argtypes = []
    result = (ctypes.c_ubyte * objlength)()

    grab.getScreen(x1, y1, w, h, result)
    return Image.frombuffer('RGB', (w, h), result, 'raw', 'RGB', 0, 1)


if __name__ == '__main__':
    from time import time
    times = [0] * 1000
    for i in range(1000):
        start = time()
        im = grab_screen(400, 400, 1000, 880)
        times[i] = time() - start
    import numpy as np
    print(np.mean(times))
    print(np.min(times))
    print(np.max(times))
    im.show()
