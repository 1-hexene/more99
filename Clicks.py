
import time
import random
import os

def likeThisVideo():
    randomX = str(random.randint(-15, 15) + 990)
    randomY = str(random.randint(-20, 20) + 1380)
    cmd = f'adb shell input tap {randomX} {randomY}'
    os.popen(cmd)
    print("我喜欢这个。")

def sendToAllFriends():
    time.sleep(random.uniform(1.0, 2.0))  # 等待动画
    randomX = str(random.randint(-15, 15) + 990)
    randomY = str(random.randint(-20, 20) + 2000)
    cmd = f'adb shell input tap {randomX} {randomY}'
    os.popen(cmd)
    
    time.sleep(random.uniform(1.0, 2.0))  # 等待动画
    randomX = str(random.randint(-15, 15) + 120)
    randomY = str(random.randint(-20, 20) + 1800)
    cmd = f'adb shell input tap {randomX} {randomY}'
    os.popen(cmd)
    time.sleep(random.uniform(1.0, 2.0))  # 等待动画

    randomX = str(random.randint(-15, 15) + 550)
    randomY = str(random.randint(-20, 20) + 2320)
    cmd = f'adb shell input tap {randomX} {randomY}'
    os.popen(cmd)
    time.sleep(random.uniform(1.0, 2.0))  # 等待动画

def nextVideo():
    time.sleep(random.uniform(1.0, 2.0))
    os.system('adb shell input touchscreen swipe 930 880 930 380')
    time.sleep(random.uniform(1.0, 2.0))
