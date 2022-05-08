import ctypes
import random
import time
import cv2
from numpy import core
from numpy.lib.function_base import select
from numpy.testing._private.utils import rand
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
        #presskey(0x2c)#pressZ
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

#被弾確認用
def Deathchack():
    DEATHCHECK_FILE = "continue.png"
    IMG_D = cv2.imread(DEATHCHECK_FILE, cv2.IMREAD_COLOR) #被弾確認用
    X = 284
    Y = 290
    W = 670
    H = 740 #撮影の座標指定
    img = ImageGrab.grab((X, Y, W, H))
    img = np.asarray(img, dtype="uint8")
    img_1 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    match_result_d = cv2.matchTemplate(img_1, IMG_D, cv2.TM_CCOEFF_NORMED)
    death_check = np.column_stack(np.where(match_result_d >= 0.75))
    if len(death_check) >= 1:
        print("被弾")
        return True
    else:
        return False

def RetryCheck():
    #あなたの腕前の画面に遷移しているかの確認
    RETRYCHECKFILE = "udemae.png"
    IMG_R = cv2.imread(RETRYCHECKFILE, cv2.IMREAD_COLOR)
    X = 284
    Y = 290
    W = 670
    H = 740 #撮影の座標指定
    img = ImageGrab.grab((X, Y, W, H))
    img = np.asarray(img, dtype="uint8")
    img_1 = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    match_result_r = cv2.matchTemplate(img_1, IMG_R, cv2.TM_CCOEFF_NORMED)
    retry_check = np.column_stack(np.where(match_result_r >= 0.75))
    if len(retry_check) >= 1:
        return True
    else:
        return False

#最初の個体を生成
def initiral_population(num, length):
    #0~17までの行動をランダムに生成
    pop = np.random.randint(0, 18, (num, length))
    return pop

#保存された個体をロード
def initial_population_load(file_name):
    pop = np.load(file_name)
    return pop

#適応度を計算＋差分の写真をとって保存
def fitness_func(pop):
    pop = pop.tolist()
    s = 0
    for i in range(len(pop)):
        print("Population: {}".format(i+1))
        t = 0
        Done = False
        Retry_check = False
        while True:
            presskey(0x2c)#pressZ
            Done = Deathchack()
            if Done:
                print("timestep: {}".format(t))
                s += t
                #リトライ用処理
                releasekey(0x2c)#releaseZ
                time.sleep(1)
                while Retry_check:
                    Retry_check = RetryCheck()
                    presskey(0x2c)
                    time.sleep(1/60)
                    releasekey(0x2c)
                    time.sleep(1)
                presskey(0x2c)
                time.sleep(1/60)
                releasekey(0x2c)#コンテニューでいいえ
                #print("いいえ")
                time.sleep(3)
                presskey(0x2c)
                time.sleep(1/60)
                releasekey(0x2c)#あなたの腕前から次へ
                #print("腕前")
                time.sleep(90/60)
                presskey(0xcd)#RIGHT
                time.sleep(1/60)
                releasekey(0xcd)#RIGHT
                time.sleep(10/60)
                presskey(0x2c)
                time.sleep(1/60)
                releasekey(0x2c)#リプレイ保存でいいえ
                #print("リプレイ")
                time.sleep(2)
                presskey(0x2c)
                time.sleep(1/60)
                releasekey(0x2c)#Start
                #print("Start")
                time.sleep(90/60)
                presskey(0x2c)
                time.sleep(1/60)
                releasekey(0x2c)#入門を押す
                #print("入門")
                time.sleep(90/60)
                presskey(0x2c)
                time.sleep(1/60)
                releasekey(0x2c)#自機選択
                #print("自機選択")
                time.sleep(90/60)
                presskey(0x2c)
                time.sleep(1/60)
                releasekey(0x2c)#装備選択
                #print("装備選択")
                #ここまでリトライ処理
                break
            if t == len(pop[i]):
                pop[i].append(random.randint(0,18))
            commandstart(pop[i][t])
            time.sleep(15/60)
            commandend(pop[i][t])
            releasekey(0x2c)#releaseZ
            t += 1
        print("average_timestep: {}".format(s/(i+1)))
    pop = np.array(pop)
    return pop

#選択された個体を使って交叉
def selection_and_crossover(pop, selected, pop_len):
    min = 0
    list_fitness = list()
    list_index = list()
    selected = list()
    #適応度が高いものを10個体並べる
    for i in range(len(pop)):
        list_fitness.append(len(pop[i]))
        list_index.append(i)
        if len(list_fitness) > 10:
            index = np.argmin(list_fitness)
            list_fitness.pop(index)
            list_index.pop(index)
    max_index = np.argmax(list_fitness)
    #次世代格納用変数
    next_gen = [[0]*len(pop[max_index]) for i in range(pop_len)]
    for i in range(0, len(pop), 3):
        selected = random.sample(list_index, 2)
        left = selected[0]
        right = selected[1]
        print("Selected: {}".format(selected))
        #2個体の長さ(適応度)を揃える
        #個体の長さが等しくなるように調整
        while len(pop[left]) != len(pop[right]):
            if len(pop[left]) < len(pop[right]):
                pop[left].append(np.random.randint(0, 18))
            elif len(pop[left]) > len(pop[right]):
                pop[right].append(np.random.randint(0, 18))
        #二点交叉
        crossover_point = [0]*2
        #交叉する位置を選ぶ
        crossover_point[0] = random.randint(1, (len(pop[left])-2))
        crossover_point[1] = random.randint((crossover_point[0]+1), (len(pop[left])-1))
        print("crossover_point: {}".format(crossover_point))
        next_gen[i] = pop[left]
        next_gen[i+1] = pop[right]
        #交叉
        next_gen[i][crossover_point[0]:crossover_point[1]], next_gen[i+1][crossover_point[0]:crossover_point[1]] = next_gen[i+1][crossover_point[0]:crossover_point[1]], next_gen[i][crossover_point[0]:crossover_point[1]]
        #一様交叉
        #引き継ぐ個体の遺伝子を決定
        crossover_pop = [random.randint(0, 1) for j in range(len(next_gen[i]))]
        for j in range(len(next_gen[i])):
            #交叉
            if crossover_pop[j] == 0:
                next_gen[i+2][j] = pop[left][j]
            else:
                next_gen[i+2][j] = pop[right][j]
    print("Crossover Done")
    return next_gen

#変異
def mutation(pop, probability):
    for i in range(len(pop)):
        if random.random() <= probability:
            print("Mutation Occured")
            mutation_point = [0]*2
            for j in range(1):
                mutation_point[j] = random.randint(0, (len(pop[i])-1))
                while mutation_point[0] == mutation_point[1]:
                    mutation_point[1] = random.randint(0, (len(pop[i])-1))
            pop[i][mutation_point[0]], pop[i][mutation_point[1]] = pop[i][mutation_point[1]], pop[i][mutation_point[0]]
    print("Mutation Done")
    return pop

def population_save(file_name, pop):
    np.save(file_name, pop)

def main():
    #パラメーターの設定
    LOAD = 0 #1でON
    LOAD_DATA = "population_gen_3.npy" #ndarray型で保存されてます
    NUMBER_POPULATION = 3 #必ず3の倍数にすること、ロードする場合ロードしたデータとここの数字を合わせること
    INITIAL_LENGTH = 10
    MUTATION_PROBABILITY = 0.01

    pop = list()
    selected = list()
    try:
        gen = 1 #途中から始める時はここを書き換える
        if LOAD >= 1:
            pop = initial_population_load(LOAD_DATA)
            print("Population loaded")
        else:
            pop = initiral_population(NUMBER_POPULATION, INITIAL_LENGTH)
            print("Initial Population Spawned")
        time.sleep(1)
        commandstart(-1)
        time.sleep(1/60)
        commandend(-1)
        while True:
            print("Generation: {}".format(gen))
            pop_tmp = list()
            pop_tmp = fitness_func(pop)
            next_gen = selection_and_crossover(pop_tmp, selected, NUMBER_POPULATION)
            next_gen = mutation(next_gen, MUTATION_PROBABILITY)
            pop = next_gen
            pop = np.array(pop) #型をlistからndarrayに変換
            gen += 1
            #各世代の適応度の平均と標準偏差を計算
            #1世代30分ぐらいかかるので毎回保存
            if gen%1 == 0:
                stats_mean = 0
                stats_sd = 0
                stats = [0]*2
                for i in range(len(pop_tmp)):
                    stats_mean += len(pop_tmp[i])
                stats_mean = stats_mean/len(pop_tmp)
                for i in range(len(pop_tmp)):
                    stats_sd += (len(pop_tmp[i])-stats_mean)**2
                stats_sd = (stats_sd/len(pop_tmp))**(1/2)
                stats[0] = stats_mean
                stats[1] = stats_sd
                population_save("population_gen_" + str(gen), pop)
                print("Population saved")
                print("Average_timestep: {}".format(stats_mean))
                print("Timestep_standard_deviation: {}".format(stats_sd))
                np.save("stats_gen_" + str(gen), stats)
    except KeyboardInterrupt:
        sys.exit()

if __name__ == "__main__":
    main()
