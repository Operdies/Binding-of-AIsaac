from ctypes import c_ulong, c_int32, byref, sizeof, windll
import win32gui
from win32process import EnumProcessModules, GetModuleFileNameEx


class Reader(object):
    def __init__(self, title='Binding'):
        self.title = title
        self.RPM = windll.kernel32.ReadProcessMemory
        win32gui.EnumWindows(self.enumHandler, None)
        PROCESS_ALL_ACCESS = 0x1F0FFF
        pid = c_ulong()
        windll.user32.GetWindowThreadProcessId(self.hwnd, byref(pid))
        self.pid = pid.value
        self.processHandle = windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, self.pid)
        addressBase = self.getAddressBase()
        pointerOffset = 0x004E6FE0  # Extracted by magic with Cheat Engine
        pointerToReferencePointer = addressBase + pointerOffset
        self.scorePointer = self.getScorePointer(pointerToReferencePointer, self.pid)

    def __del__(self):
        windll.kernel32.CloseHandle(self.processHandle)

    def getAddressBase(self):
        modules = EnumProcessModules(self.processHandle)
        for n_mod in modules:
            modName = GetModuleFileNameEx(self.processHandle, n_mod)
            if "isaac-ng" in modName:
                return n_mod

    def getScore(self):
        score = c_ulong()
        bytesRead = c_ulong()
        self.RPM(self.processHandle, self.scorePointer, byref(score), sizeof(score), byref(bytesRead))
        return score.value

    def enumHandler(self, hwnd, lParam):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if self.title in window_text:
                self.hwnd = hwnd
                print('Found: ', window_text)

    def getScorePointer(self, refP, pid):
        ReadProcessMemory = windll.kernel32.ReadProcessMemory
        scorePointer = c_int32()
        bytesRead = c_ulong()
        ReadProcessMemory(self.processHandle, refP, byref(scorePointer), sizeof(scorePointer), byref(bytesRead))
        return scorePointer.value + 0x253CF8  # Magic number extracted with  Cheat Engine


if __name__ == '__main__':
    reader = Reader()
    from time import sleep
    for i in range(0, 100):
        print(reader.getScore())
        sleep(0.1)

