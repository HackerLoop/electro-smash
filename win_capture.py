#!/usr/bin/env python3
# pylint: disable=no-member
import logging
import sys

import numpy as np
import os.path
import time
import math
import win32gui, win32ui, win32con, win32api
import requests
import pyautogui

try:
    import cv2
except ImportError:
    sys.stderr.write("requires opencv-python")
    raise

P1p = 0
P2p = 0

class winCapture:
    def __init__(self):
        #self.hwnd = win32gui.FindWindow(None,'Windowed Projector (Preview)')
        self.hwnd = win32gui.FindWindow(None,'Projecteur fenêtré (aperçu)')
        print(self.hwnd)
        self.w = 0
        self.h = 0
        self.inner_w = 0
        self.inner_h = 0
        self.hwndDC = win32gui.GetWindowDC(self.hwnd)
        self.mfcDC = win32ui.CreateDCFromHandle(self.hwndDC)
        self.saveDC = self.mfcDC.CreateCompatibleDC()

    def getSize(self):
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        self.w = right - left
        self.h = bot - top
        #print (left, top, right, bot)
        left, top, right, bot = win32gui.GetClientRect(self.hwnd)
        self.inner_w = right - left
        self.inner_h = bot - top
        print (left, top, right, bot)

    def getframe(self):
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(self.mfcDC, self.w, self.h)
        self.saveDC.SelectObject(saveBitMap)
        self.saveDC.BitBlt((0, 0), (self.w, self.h), self.mfcDC, (0, 0), win32con.SRCCOPY)
        #saveBitMap.SaveBitmapFile(self.saveDC, 'test.jpg')
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        img = np.frombuffer(signedIntsArray, dtype='uint8')
        img.shape = (self.h,self.w,4)
        win32gui.DeleteObject(saveBitMap.GetHandle())
        chromeUrlBar = 37
        correction_obs = -30
        # border
        x = math.floor((self.w - self.inner_w)/2)
        # border & chromeUrlBar
        y = self.h - self.inner_h - x #+ chromeUrlBar
        w = self.inner_w
        h = self.inner_h #- chromeUrlBar
        img = img[y:y+h, x:x+w]
        rectangle = np.array([[253, 124], [890, 143]])
        return (img,
        img[rectangle[0][1]:rectangle[1][1], rectangle[0][0]:rectangle[1][0]],
        img[:,::-1][rectangle[0][1]:rectangle[1][1], rectangle[0][0]:rectangle[1][0]])

    def stop(self):
        self.mfcDC.DeleteDC()
        self.saveDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.hwndDC)

def matchTemplate(percents):
    global P1p, P2p
    p1Percent, p2Percent = percents
    if p1Percent < P1p:
        P1p = p1Percent
        print(P1p,P2p)
        try:
            #requests.post("http://localhost:3000/degats", json={'j1': P1p, 'j2': P2p})
            #requests.post("http://localhost:3000/degats", json={'pulse': 1, 'lvl': round(P1p/100)}, timeout=1.5)
            requests.post("http://192.168.43.47", json={'pulse': 1, 'lvl': round(P1p/100)}, timeout=1.5)
            print("ok")
        except:
            print("fail !!")
    if p2Percent < P2p:
        P2p = p2Percent
        print(P1p,P2p)
        try:
            #requests.post("http://localhost:3000/degats", json={'j1': P1p, 'j2': P2p}, timeout=1.5)
            #requests.post("http://localhost:3000/degats", json={'pulse': 2, 'lvl': round(P2p/100)}, timeout=1.5)
            requests.post("http://192.168.43.47", json={'pulse': 2, 'lvl': round(P2p/100)}, timeout=1.5)
            print("ok")
        except:
            print("fail !!")

def main():
    win = winCapture()
    win.getSize()
    fps = 30
    frame_time = int((1.0 / fps) * 1000.0)
    template = []
    for num in range(10):
        template.append(cv2.imread('./template/'+str(num)+'.png',0))
    while True:
        try:
            (frame,frame_1p,frame_2p) = win.getframe()
            frame_p = np.concatenate((frame_1p, frame_2p), axis=1)
            percents = get_prop(frame_1p), get_prop(frame_2p)
            matchTemplate(percents)
            #cv2.imshow('frame', frame)

            frame_p = cv2.resize(frame_p, (0,0), fx=3, fy=3)
            cv2.imshow('percent', frame_p)
            if cv2.waitKey(frame_time*10) & 0xFF == ord('q'):
                win.stop()
                break
        except KeyboardInterrupt:
            win.stop()
            break
    cv2.destroyAllWindows()

# max_callibration = None

def get_prop(rgb_img):
    img = rgb_img[:,:,1]
    # img = cv2.GaussianBlur(img, (3,3), 1)
    N = 3
    img = np.average(img, axis=0)
    img = np.convolve(img, np.ones(N)/N, mode='valid')

    global max_callibration
    if max_callibration is None:
        max_callibration = img.max()
    #normalize
    img = (img - img.min())/(max_callibration - img.min())

    results = np.where(np.gradient(img) > .1)[0]
    return (1 - np.where(np.gradient(img) > .1)[0][0] / img.size)

# def main():
#     img = cv2.imread('test.png')
#     rectangle = np.array([[205, 126], [884, 146]])
#     img_left = img[rectangle[0][1]:rectangle[1][1], rectangle[0][0]:rectangle[1][0]]
#     left = get_prop(img_left)

#     img = img[:,::-1]
#     img_right = img[rectangle[0][1]:rectangle[1][1], rectangle[0][0]:rectangle[1][0]]
#     right = get_prop(img_right)

#     print(left * 100, '%', right * 100, '%')


if __name__ == "__main__":
    time.sleep(2)
    main()
