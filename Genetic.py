import ctypes
import random
import cv2
import pynput
import sys
import numpy as np

from PIL import ImageGrab

#コマンド入力用(強化学習からの使いまわし)
SENDINPUT = ctypes.windll.user32.SendInput

PUL = ctypes.POINTER(ctypes.c_ulong)
class KeyBdInput(ctypes.Structure):
    _fields_ = [("wvk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlagss", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_ushort),
                ("wParamH", ctypes.c_ushort)]

class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_ulong),
                ("dy", ctypes.c_ulong),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]

class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]

class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]

def presskey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SENDINPUT(1, ctypes.pointer(x), ctypes.sizeof(x))

def releasekey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SENDINPUT(1, ctypes.pointer(x), ctypes.sizeof(x))

def commandstart(action):
    if action == -1:
        presskey(0x01)#ESC
    elif action == 0:
        pass
    elif action == 1:
        presskey(0xcb)#LEFT
    elif action == 2:
        presskey(0xc8)#UP
    elif action == 3:
        presskey(0xcd)#RIGHT
    elif action == 4:
        presskey(0xd0)#DOWN
    elif action == 5:
        presskey(0xcb)#LEFT
        presskey(0xc8)#UP
    elif action == 6:
        presskey(0xc8)#UP
        presskey(0xcd)#RIGHT
    elif action == 7:
        presskey(0xcd)#RIGHT
        presskey(0xd0)#DOWN
    elif action == 8:
        presskey(0xd0)#DOWN
        presskey(0xcb)#LEFT
    elif action == 9:
        presskey(0x2a)#LSHIFT
    elif action == 10:
        presskey(0x2a)#LSHIFT
        presskey(0xcb)#LEFT
    elif action == 11:
        presskey(0x2a)#LSHIFT
        presskey(0xc8)#UP
    elif action == 12:
        presskey(0x2a)#LSHIFT
        presskey(0xcd)#RIGHT
    elif action == 13:
        presskey(0x2a)#LSHIFT
        presskey(0xd0)#DOWN
    elif action == 14:
        presskey(0x2a)#LSHIFT
        presskey(0xcb)#LEFT
        presskey(0xc8)#UP
    elif action == 15:
        presskey(0x2a)#LSHIFT
        presskey(0xc8)#UP
        presskey(0xcd)#RIGHT
    elif action == 16:
        presskey(0x2a)#LSHIFT
        presskey(0xcd)#RIGHT
        presskey(0xd0)#DOWN
    elif action == 17:
        presskey(0x2a)#LSHIFT
        presskey(0xd0)#DOWN
        presskey(0xcb)#LEFT

def commandend(action):
    if action == -1:
        releasekey(0x01)#ESC
    elif action == 0:
        #releasekey(0x2c)#Z
        pass
    elif action == 1:
        releasekey(0xcb)#LEFT
    elif action == 2:
        releasekey(0xc8)#UP
    elif action == 3:
        releasekey(0xcd)#RIGHT
    elif action == 4:
        releasekey(0xd0)#DOWN
    elif action == 5:
        releasekey(0xcb)#LEFT
        releasekey(0xc8)#UP
    elif action == 6:
        releasekey(0xc8)#UP
        releasekey(0xcd)#RIGHT
    elif action == 7:
        releasekey(0xcd)#RIGHT
        releasekey(0xd0)#DOWN
    elif action == 8:
        releasekey(0xd0)#DOWN
        releasekey(0xcb)#LEFT
    elif action == 9:
        #LSHIFT
        releasekey(0x2a)#LSHIFT
    elif action == 10:
        releasekey(0x2a)#LSHIFT
        releasekey(0xcb)#LEFT
    elif action == 11:
        releasekey(0x2a)#LSHIFT
        releasekey(0xc8)#UP
    elif action == 12:
        releasekey(0x2a)#LSHIFT
        releasekey(0xcd)#RIGHT
    elif action == 13:
        releasekey(0x2a)#LSHIFT
        releasekey(0xd0)#DOWN
    elif action == 14:
        releasekey(0x2a)#LSHIFT
        releasekey(0xcb)#LEFT
        releasekey(0xc8)#UP
    elif action == 15:
        releasekey(0x2a)#LSHIFT
        releasekey(0xc8)#UP
        releasekey(0xcd)#RIGHT
    elif action == 16:
        releasekey(0x2a)#LSHIFT
        releasekey(0xcd)#RIGHT
        releasekey(0xd0)#DOWN
    elif action == 17:
        releasekey(0x2a)#LSHIFT
        releasekey(0xd0)#DOWN
        releasekey(0xcb)#LEFT

#最初の個体を生成
def initiral_population(num, length):
    pop = np.random.randint(0, 18, (num, length))
    return pop

#保存された個体をロード
def initial_population_load():
    pop = np.load("population.npy")
    return pop

#適応度を計算＋差分の写真をとって保存
def fitness_func():
    pass

#適応度に応じて選択
def selection():
    pass

#選択された個体を使って交叉
def crossover():
    pass

#変異
def mutation():
    pass

def population_save(file_name, pop):
    np.save(file_name, pop)

def main():
    LOAD = 1
    pop = list()
    try:
        if LOAD >= 1:
            pop = initial_population_load()
            print(pop)
        else:
            pop = initiral_population(5, 10)
            print(pop)
        fitness_func()
        selection()
        crossover()
        mutation()
        population_save("population", pop)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()
