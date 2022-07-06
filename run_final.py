# coding: utf8

import time
from datetime import datetime
from decimal import Decimal


import RPi.GPIO as GPIO
import numpy as np

import cv2

print('start program')
print('init')
# GPIO 設定
GPIO.setmode(GPIO.BOARD)
# GPIO Err Message
GPIO.setwarnings(False)

B_N1 = 11  # GPIO11
B_N2 = 12  # GPIO12
B_N3 = 13  # GPIO13
B_N4 = 15  # GPIO15

# 後驅動板
GPIO.setup(B_N1, GPIO.OUT)  # back wheel right
GPIO.setup(B_N2, GPIO.OUT)  # back wheel right
GPIO.setup(B_N3, GPIO.OUT)  # back wheel left
GPIO.setup(B_N4, GPIO.OUT)  # back wheel left

F_N1 = 32  # GPIO32
F_N2 = 36  # GPIO36
F_N3 = 38  # GPIO38
F_N4 = 40  # GPIO40

# 前驅動板
GPIO.setup(F_N1, GPIO.OUT)  # front wheel right
GPIO.setup(F_N2, GPIO.OUT)  # front wheel right
GPIO.setup(F_N3, GPIO.OUT)  # front wheel left
GPIO.setup(F_N4, GPIO.OUT)  # front wheel left

PWM_Freq = 40

# 設定馬達初始頻率
pwmB_N1 = GPIO.PWM(B_N1, PWM_Freq)
pwmB_N2 = GPIO.PWM(B_N2, PWM_Freq)
pwmB_N3 = GPIO.PWM(B_N3, PWM_Freq)
pwmB_N4 = GPIO.PWM(B_N4, PWM_Freq)

pwmF_N1 = GPIO.PWM(F_N1, PWM_Freq)
pwmF_N2 = GPIO.PWM(F_N2, PWM_Freq)
pwmF_N3 = GPIO.PWM(F_N3, PWM_Freq)
pwmF_N4 = GPIO.PWM(F_N4, PWM_Freq)

# 設定馬達能量
pwmB_N1.start(0)
pwmB_N2.start(0)
pwmB_N3.start(0)
pwmB_N4.start(0)

pwmF_N1.start(0)
pwmF_N2.start(0)
pwmF_N3.start(0)
pwmF_N4.start(0)

pwn_Power = 10  # 能量


def MoveForward(x):
    print('MoveForward:')
    # RIGHT = N1, N2
    # LEFT = N3, N4

    pwmB_N1.ChangeDutyCycle(0)  # 0
    pwmB_N3.ChangeDutyCycle(0)  # 0
    pwmF_N1.ChangeDutyCycle(0)  # 0
    pwmF_N3.ChangeDutyCycle(0)  # 0

    pwmB_N2.ChangeDutyCycle(pwn_Power*x)  # 1
    pwmB_N4.ChangeDutyCycle(pwn_Power*x)  # 1
    pwmF_N2.ChangeDutyCycle(pwn_Power*x)  # 1
    pwmF_N4.ChangeDutyCycle(pwn_Power*x)  # 1


def MoveLeft(x):
    print('MoveLeft()',x)
    pwmB_N1.ChangeDutyCycle(0)  # 0
    pwmB_N2.ChangeDutyCycle(abs(45*x))  # 1
    pwmB_N3.ChangeDutyCycle(abs(20*x))  # 0
    pwmB_N4.ChangeDutyCycle(0)  # 0
     # ---------------------------
    pwmF_N1.ChangeDutyCycle(0)  # 0
    pwmF_N2.ChangeDutyCycle(abs(45*x))  # 1
    pwmF_N3.ChangeDutyCycle(abs(20*x))  # 0
    pwmF_N4.ChangeDutyCycle(0)  # 0

# def MoveLeftV(x):
#     print('MoveLeft()')
#     pwmB_N1.ChangeDutyCycle(0)  # 0
#     pwmB_N2.ChangeDutyCycle(abs(55*x))  # 1
#     pwmB_N3.ChangeDutyCycle(abs(45*x))  # 0
#     pwmB_N4.ChangeDutyCycle(0)  # 0
#      # ---------------------------
#     pwmF_N1.ChangeDutyCycle(0)  # 0
#     pwmF_N2.ChangeDutyCycle(abs(45*x))  # 1
#     pwmF_N3.ChangeDutyCycle(abs(45*x))  # 0
#     pwmF_N4.ChangeDutyCycle(0)  # 0

def MoveRightV(x):
    print('MoveRight()')
    pwmB_N1.ChangeDutyCycle(abs(65*x))  # 0
    pwmB_N2.ChangeDutyCycle(0)  # 0
    pwmB_N3.ChangeDutyCycle(0)  # 0
    pwmB_N4.ChangeDutyCycle(abs(65*x))  # 1
     # ---------------------------
    pwmF_N1.ChangeDutyCycle(abs(65*x))  # 0
    pwmF_N2.ChangeDutyCycle(0)  # 0
    pwmF_N3.ChangeDutyCycle(0)  # 0
    pwmF_N4.ChangeDutyCycle(abs(65*x))  # 1

def MoveRight(x):
    print('MoveRight()',x)
    pwmB_N1.ChangeDutyCycle(abs(20*x))  # 0
    pwmB_N2.ChangeDutyCycle(0)  # 0
    pwmB_N3.ChangeDutyCycle(0)  # 0
    pwmB_N4.ChangeDutyCycle(abs(45*x))  # 1
     # ---------------------------
    pwmF_N1.ChangeDutyCycle(abs(20*x))  # 0
    pwmF_N2.ChangeDutyCycle(0)  # 0
    pwmF_N3.ChangeDutyCycle(0)  # 0
    pwmF_N4.ChangeDutyCycle(abs(45*x))  # 1


def MoveStop():
    # print('MoveStop()')
    pwmB_N1.ChangeDutyCycle(0)  # 0
    pwmB_N2.ChangeDutyCycle(0)  # 0
    pwmB_N3.ChangeDutyCycle(0)  # 0
    pwmB_N4.ChangeDutyCycle(0)  # 0
    # ---------------------------
    pwmF_N1.ChangeDutyCycle(0)  # 0
    pwmF_N2.ChangeDutyCycle(0)  # 0
    pwmF_N3.ChangeDutyCycle(0)  # 0
    pwmF_N4.ChangeDutyCycle(0)  # 0


# center定義
center = 320
# 打開攝影機，圖像尺寸640*480（長*高），opencv存儲值爲480*640（行*列）
cap = cv2.VideoCapture(0)

# 要觀看影像的X座標位置右側 (640x480)
imgYC = 320    # 320

image_Y = 20
image_Y2 = 30
# image_Y3 = 360
# image_Y4 = 350



print('running')

outT=0
mode =0
switch =0
MoveForward(1)
MoveForward(1)
MoveForward(1)

while mode ==0:

    ret, frame = cap.read()
    # print('ret:', ret)  # 正確讀到影像時，回傳TRUE
    # print('frame:', frame)    # RAWImage資料
    if not ret:
        print("error")

    # 測試輸出影像
    filename = 'photo/' +'camera_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpg'
    # print('filename:', filename)
    # cv2.imwrite(filename, frame)

    # 轉化爲灰度圖
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    filename = 'photo/' +'gray_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpg'
    # print('filename:', filename)
    # cv2.imwrite(filename, gray)
    

    
    # 大津法二值化
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    # cv2.blur(gray, (5,5))
#     dst = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 12)
    # print('retval:', retval)    # ??
    # print ('dst:', dst)       # 二值化的結果矩陣

    


    # filename = 'thre_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpg'
    # print('filename:', filename)
    # cv2.imwrite(filename, dst)

    # 膨脹，白區域變大
    # dst = cv2.dilate(dst, None, iterations=2)
    # 腐蝕，白區域變小[OK]黑色區域明顯顯示
    dst = cv2.erode(dst, None, iterations=6)
    filename6 = 'photo/' +'thre6_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpg'
    # print('filename:', filename6)
    cv2.imwrite(filename6, cv2.hconcat([dst, gray]))

    pixelmove1 = 100
    pixelmove2 = 90
    pixelmove3 = 120

    imgYR1 = imgYC + pixelmove1
    imgYR2 = imgYC + pixelmove2
    imgYR3 = imgYC + pixelmove3

    imgYL1 = imgYC - pixelmove1
    imgYL2 = imgYC - pixelmove2
    imgYL3 = imgYC - pixelmove3


    pixel_C1 = dst[image_Y][imgYC]
    
    pixel_R1 = dst[image_Y][imgYR1]
    pixel_R2 = dst[image_Y2][imgYR2]
    pixel_R3 = dst[image_Y][imgYR3]
    # pixel_R4 = dst[image_Y4][imgYR2] 
    
    pixel_L1 = dst[image_Y][imgYL1]
    pixel_L2 = dst[image_Y2][imgYL2]
    pixel_L3 = dst[image_Y][imgYL3]
    # pixel_L4 = dst[image_Y4][imgYL2]
#--------------------------------------

    print('single')
    MoveForward(0.6)
    if(pixel_L1 == 255 and  pixel_R1 == 255) :
       MoveForward(0.8)
    if( pixel_L1 == 0 ) :
        MoveLeft(0.6)
    if( pixel_R1 == 0 ) :
        MoveRight(0.6)
    if(pixel_L1==0 and pixel_L2 == 0):
        MoveLeft(0.8)
    if(pixel_R1==0 and pixel_R2==0):
        MoveRight(0.8)
    
    if(pixel_R1 == 0 and pixel_R2== 0 and pixel_R3 == 0 ):
        switch =1
        mode =1
        break
    elif(pixel_L1==0 and pixel_L2==0 and pixel_L3 ==0 and pixel_R1==0 and pixel_R2==0 and pixel_R3 ==0):
        switch =0
        mode =1
        break

MoveForward(1)
MoveForward(1)
MoveRight(1.2)

MoveForward(0.5)
print('in')


while switch == 1:
    print('double')

    ret, frame = cap.read()
    # print('ret:', ret)  # 正確讀到影像時，回傳TRUE
    # print('frame:', frame)    # RAWImage資料
    if not ret:
        print("error")

    # 測試輸出影像
    filename = 'photo/' +'camera_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpg'
    # print('filename:', filename)
    # cv2.imwrite(filename, frame)

    # 轉化爲灰度圖
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    filename = 'photo/' +'gray_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpg'
    # print('filename:', filename)
    # cv2.imwrite(filename, gray)
    

    
    # 大津法二值化
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    # cv2.blur(gray, (5,5))
#     dst = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 13, 12)
    # print('retval:', retval)    # ??
    # print ('dst:', dst)       # 二值化的結果矩陣

    


    # filename = 'thre_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpg'
    # print('filename:', filename)
    # cv2.imwrite(filename, dst)

    # 膨脹，白區域變大
    # dst = cv2.dilate(dst, None, iterations=2)
    # 腐蝕，白區域變小[OK]黑色區域明顯顯示
    dst = cv2.erode(dst, None, iterations=6)
    filename6 = 'photo/' +'thre6_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpg'
    # print('filename:', filename6)
    cv2.imwrite(filename6, cv2.hconcat([dst, gray]))

    pixelmove1 = 130
    pixelmove2 = 110
    pixelmove3 = 105

    
    if( pixel_L1 == 0 ) :
        MoveLeft(0.6)
    if( pixel_R1 == 0 ) :
        MoveRight(0.6)
    if(pixel_L1==0 and pixel_L2 == 0):
        MoveLeft(0.8)
    if(pixel_R1==0 and pixel_R2==0):
        MoveRight(0.8) 
    if(pixel_L1==0 and pixel_L2==0 and pixel_L3 ==0 and pixel_R1==0 and pixel_R2==0 and pixel_R3 ==0):
        switch =0
        mode =0
        break
# coding=utf8

import pygame
# from pygame.locals import *
import RPi.GPIO as GPIO
from time import sleep


pwn_Power = 50  # 能量
pwn_Rate = 50  # 倍率


def MoveForward(axs1):
    print('MoveForward:')
    # RIGHT = N1, N2
    # LEFT = N3, N4

    pwmB_N1.ChangeDutyCycle(0)  # 0
    pwmB_N3.ChangeDutyCycle(0)  # 0
    pwmF_N1.ChangeDutyCycle(0)  # 0
    pwmF_N3.ChangeDutyCycle(0)  # 0

    pwmB_N2.ChangeDutyCycle(abs(axs1 * pwn_Power)*2)  # 1
    pwmB_N4.ChangeDutyCycle(abs(axs1 * pwn_Power)*2)  # 1
    pwmF_N2.ChangeDutyCycle(abs(axs1 * pwn_Power)*2)  # 1
    pwmF_N4.ChangeDutyCycle(abs(axs1 * pwn_Power)*2)  # 1
        


def MoveBack(axs1):
    print('MoveBack:')

    pwmB_N2.ChangeDutyCycle(0)  # 0
    pwmB_N4.ChangeDutyCycle(0)  # 0
    pwmF_N2.ChangeDutyCycle(0)  # 0
    pwmF_N4.ChangeDutyCycle(0)  # 0
    
    pwmB_N1.ChangeDutyCycle(abs(axis1 * pwn_Power)*2)  # 1
    pwmB_N3.ChangeDutyCycle(abs(axis1 * pwn_Power)*2)  # 1
    pwmF_N1.ChangeDutyCycle(abs(axis1 * pwn_Power)*2)  # 1
    pwmF_N3.ChangeDutyCycle(abs(axis1 * pwn_Power)*2)  # 1


def MoveStop():
    # print('MoveStop()')
    pwmB_N1.ChangeDutyCycle(0)  # 0
    pwmB_N2.ChangeDutyCycle(0)  # 0
    pwmB_N3.ChangeDutyCycle(0)  # 0
    pwmB_N4.ChangeDutyCycle(0)  # 0
    # ---------------------------
    pwmF_N1.ChangeDutyCycle(0)  # 0
    pwmF_N2.ChangeDutyCycle(0)  # 0
    pwmF_N3.ChangeDutyCycle(0)  # 0
    pwmF_N4.ChangeDutyCycle(0)  # 0




def MoveLeft(x):
    print('MoveLeft()')
    pwmB_N1.ChangeDutyCycle(0)  # 0
    pwmB_N2.ChangeDutyCycle(abs(80*x))  # 1
    pwmB_N3.ChangeDutyCycle(abs(70*x))  # 0
    pwmB_N4.ChangeDutyCycle(0)  # 0
     # ---------------------------
    pwmF_N1.ChangeDutyCycle(0)  # 0
    pwmF_N2.ChangeDutyCycle(abs(80*x))  # 1
    pwmF_N3.ChangeDutyCycle(abs(70*x))  # 0
    pwmF_N4.ChangeDutyCycle(0)  # 0


def MoveRight(x):
    print('MoveRight()')
    pwmB_N1.ChangeDutyCycle(abs(70*x))  # 0
    pwmB_N2.ChangeDutyCycle(0)  # 0
    pwmB_N3.ChangeDutyCycle(0)  # 0
    pwmB_N4.ChangeDutyCycle(abs(80*x))  # 1
     # ---------------------------
    pwmF_N1.ChangeDutyCycle(abs(70*x))  # 0
    pwmF_N2.ChangeDutyCycle(0)  # 0
    pwmF_N3.ChangeDutyCycle(0)  # 0
    pwmF_N4.ChangeDutyCycle(abs(80*x))  # 1


# TEST RUNNING
# MoveForward()

# 工具初始化
pygame.init()


# 搖桿初始化
pygame.joystick.init()


if pygame.joystick.get_init():
    #print('JoyStick Count:', pygame.joystick.get_count())

    # 設定使用搖桿0
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # 取得搖桿名稱
    name = joystick.get_name()
    #print('JoyStick Name:', name)

    # 取得搖桿軸數量
    numaxes = joystick.get_numaxes()
    #print('axes Count:', numaxes)

    # 取得搖桿按鈕數量
    numbuttons = joystick.get_numbuttons()
    #print('button Count:', numbuttons)

    BUTTONB_DOWN = False
    BUTTONY_DOWN = False

while True:

    event = pygame.event.get()

    axis1 = joystick.get_axis(1)
    axis2 = joystick.get_axis(2)
    # axis6 = joystick.get_axis(6)
    # axis7 = joystick.get_axis(7)

    BUTTONB = joystick.get_button(1)
    BUTTONY = joystick.get_button(4)
    BUTTONRB = joystick.get_button(6)
    BUTTONLB = joystick.get_button(7)
    

    if (BUTTONB):
        BUTTONB_DOWN = True
    else :
        if(BUTTONB_DOWN):
            PWM_Freq = 25
            print('slow mode')
            pwmB_N1.ChangeFrequency(PWM_Freq)
            pwmB_N2.ChangeFrequency(PWM_Freq)
            pwmB_N3.ChangeFrequency(PWM_Freq)
            pwmB_N4.ChangeFrequency(PWM_Freq)

            pwmF_N1.ChangeFrequency(PWM_Freq)
            pwmF_N2.ChangeFrequency(PWM_Freq)
            pwmF_N3.ChangeFrequency(PWM_Freq)
            pwmF_N4.ChangeFrequency(PWM_Freq)
            BUTTONB_DOWN = False
            

    if (BUTTONY):
        BUTTONY_DOWN = True
    else:
        if(BUTTONY_DOWN):
            PWM_Freq = 100
            print('fast mode')
            pwmB_N1.ChangeFrequency(PWM_Freq)
            pwmB_N2.ChangeFrequency(PWM_Freq)
            pwmB_N3.ChangeFrequency(PWM_Freq)
            pwmB_N4.ChangeFrequency(PWM_Freq)

            pwmF_N1.ChangeFrequency(PWM_Freq)
            pwmF_N2.ChangeFrequency(PWM_Freq)
            pwmF_N3.ChangeFrequency(PWM_Freq)
            pwmF_N4.ChangeFrequency(PWM_Freq)
            BUTTONY_DOWN = False

    
    
    
    if axis1 < 0 : 
        MoveForward(axis1)
    elif axis1 > 0 :
        MoveBack(axis1)
    elif axis2 < 0 : 
        MoveLeft(axis2)
    elif axis2 > 0 :
        MoveRight(axis2)
    elif BUTTONRB :
        MoveForward(0.3)
    elif BUTTONLB :
        MoveForward(1)
    # elif axis6 > 0 :
    #     MoveRight(0.3)
    # elif axis6 < 0 :
    #     MoveLeft(0.3)
    # elif axis7 < 0 :
    #     MoveForward(0.3)
    # elif axis7 > 0 :
    #     MoveBack(0.3)
    else:
        MoveStop()

    # sleep(0.1) 

    

    
    
    
    
    time.sleep(0.05)
    # outT+=1
    # if outT>80:
    #     break
#     cv2.imshow('apple', show)
    # cv2.imshow('banana', dst)
    # ch = cv2.waitKey(1)
#     if ch==ord('q'):
#         break
    

    # break


# 釋放清理
cap.release()
cv2.destroyAllWindows()
#pwm1.stop()
#pwm2.stop()
#pwm3.stop()
#pwm4.stop()
#pwm5.stop()
#pwm6.stop()
#pwm7.stop()
#pwm8.stop()
pwmB_N1.stop()
pwmB_N2.stop()
pwmB_N3.stop()
pwmB_N4.stop()

pwmF_N1.stop()
pwmF_N2.stop()
pwmF_N3.stop()
pwmF_N4.stop()
GPIO.cleanup()
