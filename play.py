import os
import time
import random
import threading
import queue
from ultralytics import YOLO
import cv2
from followIcon import getRedWhite, ssimCheck
from Clicks import *

# 创建队列用于线程间通信
action_queue = queue.Queue()
pause_detection = threading.Event()


def scaleImage(image, scale):
    width = int(image.shape[1] * scale)
    height = int(image.shape[0] * scale)
    return cv2.resize(image, (width, height))

# 检测线程
def detection_worker():
    results = None
    model = YOLO("runs/classify/train/weights/best.pt")
    cam = cv2.VideoCapture(0)
    redT = cv2.imread('template/red.png', cv2.IMREAD_GRAYSCALE)
    whiteT = cv2.imread('template/white.png', cv2.IMREAD_GRAYSCALE)

    eroticFrameCount = 0
    liveStreamFrameCount = 0
    startime = time.time()
    randomTimeout = random.uniform(5, 10)
    continueFlag = False

    while True:
        continueFlag = False
        ret, frame = cam.read()
        if not ret:
            continue
        
        frame = scaleImage(frame, 0.5)
        red, white = getRedWhite(frame)

        # 暂停检测？
        if pause_detection.is_set():
            # time.sleep(0.01)
            continueFlag = True

        # 检测关注加号
        if liveStreamFrameCount >= 10:
            # print("直播帧疑似有点多了")
            continueFlag = True
        
        if ssimCheck(red, redT) > 0.7 and ssimCheck(white, whiteT)> 0.7:
            frameRT = cv2.rectangle(frame, (460, 583), (533, 670), (0,255,0), 10)
            liveStreamFrameCount = 0
        else:
            frameRT = cv2.rectangle(frame, (460, 583), (533, 670), (0,0,255), 10)
            liveStreamFrameCount = 10 if liveStreamFrameCount >= 10 else liveStreamFrameCount + 1
        
        frameRT = cv2.putText(frameRT, 'LiveStream = ' + str(liveStreamFrameCount) , (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        if not pause_detection.is_set() and not continueFlag:
            results = model(frame, verbose=False)[0]
            if results:
                probs = results.probs
                classIndex = probs.top1
                className = results.names[classIndex]
                classConfidence = probs.data[classIndex]

                if className == 'erotic':
                    textColor = (0, 255, 0)
                else:
                    textColor = (0, 0, 255)

                frameRT = cv2.putText(frameRT, f'{className} : {int(classConfidence * 100)} %' , (10, 130), cv2.FONT_HERSHEY_SIMPLEX, 1, textColor, 2, cv2.LINE_AA)

                frameRT = cv2.putText(frameRT,  className + " = "+ str(eroticFrameCount), (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, textColor, 2, cv2.LINE_AA)
                if classConfidence >= 0.75 and className == 'erotic':
                    eroticFrameCount += 1
                else:
                    eroticFrameCount = 0 if eroticFrameCount < 5 else eroticFrameCount - 5
        else:
            frameRT = cv2.putText(frameRT, "INFERENCE PAUSE" , (10, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2, cv2.LINE_AA)
        

        cv2.imshow('CURRENT FRAME', frameRT)
        cv2.imshow('red', red)
        cv2.imshow('white', white)


        if eroticFrameCount >= 30 and not continueFlag and liveStreamFrameCount == 0:
            action_queue.put("like")
            action_queue.put("send")
            action_queue.put("next")
            eroticFrameCount = 0
            liveStreamFrameCount = 0
            startime = time.time()
            continue
    
        currtime = time.time()
        if currtime - startime >= randomTimeout:
            action_queue.put("next")
            eroticFrameCount = 0
            liveStreamFrameCount = 0
            print("不喜欢这个。")
            startime = currtime
            randomTimeout = random.uniform(5, 10)

        if cv2.waitKey(1) == ord('q'):
            action_queue.put("quit")
            break

    cam.release()
    cv2.destroyAllWindows()


def click_worker():
    while True:
        action = action_queue.get()
        if action == "like":
            pause_detection.set()
            likeThisVideo()
            pause_detection.clear()
        elif action == "next":
            pause_detection.set()
            nextVideo()
            # empty queue
            while not action_queue.empty():
                action_queue.get()
            
            pause_detection.clear()
        elif action == "send":
            pause_detection.set()
            sendToAllFriends()
            
            pause_detection.clear()
        elif action == "quit":
            break
        action_queue.task_done()



def main():
    # 启动抖音
    package_name = 'com.ss.android.ugc.aweme'
    activity_name = 'com.ss.android.ugc.aweme.splash.SplashActivity'
    os.system(f'adb shell am start -n {package_name}/{activity_name}')
    time.sleep(5)

    # 启动两个线程
    click_thread = threading.Thread(target=click_worker, daemon=True)
    detect_thread = threading.Thread(target=detection_worker)

    click_thread.start()
    detect_thread.start()

    detect_thread.join()  # 等待检测线程结束
    action_queue.join()   # 等待所有点击动作完成

if __name__ == '__main__':
    main()
