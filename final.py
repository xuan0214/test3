# coding:utf-8
from pickle import FALSE, TRUE
import RPi.GPIO as GPIO
import sys

import time
from datetime import datetime
from time import sleep

import cv2
import numpy as np

import pygame

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

# 工具初始化
pygame.init()

# 搖桿初始化
pygame.joystick.init()

#自走循跡

# 定義引腳
#右前輪

F_N1 = 32 #PIN38
F_N2 = 36 #PIN40

#左前輪

F_N3 = 38 #PIN33
F_N4 = 40 #PIN34


#右後輪
B_N1 = 11 #PIN24
B_N2 = 12 #PIN26

#左後輪

B_N3 = 13 #PIN19
B_N4 = 15 #PIF_N3


# 設置GPIO口爲輸出
# GPIO.setup(EN1, GPIO.OUT)
GPIO.setup(F_N1, GPIO.OUT)
GPIO.setup(F_N2, GPIO.OUT)
GPIO.output(F_N1,GPIO.LOW)
GPIO.output(F_N2,GPIO.LOW)

# GPIO.setup(EN2, GPIO.OUT)
GPIO.setup(F_N3, GPIO.OUT)
GPIO.setup(F_N4, GPIO.OUT)
GPIO.output(F_N3,GPIO.LOW)
GPIO.output(F_N4,GPIO.LOW)

# GPIO.setup(EN3, GPIO.OUT)
GPIO.setup(B_N1, GPIO.OUT)
GPIO.setup(B_N2, GPIO.OUT)
GPIO.output(B_N1,GPIO.LOW)
GPIO.output(B_N2,GPIO.LOW)

# GPIO.setup(EN4, GPIO.OUT)
GPIO.setup(B_N3, GPIO.OUT)
GPIO.setup(B_N4, GPIO.OUT)
GPIO.output(B_N3,GPIO.LOW)
GPIO.output(B_N4,GPIO.LOW)

PWM_Freq = 500

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


# # 設置PWM波,頻率爲500Hz
# pwmB_N2 = GPIO.PWM(32, 500)
# pwmB_N4 = GPIO.PWM(38, 500)
# pwmF_N2 = GPIO.PWM(11, 500)
# pwmF_N4 = GPIO.PWM(13, 500)

# # p波控制初始化
# pwmB_N2.start(0)
# pwmB_N4.start(0)
# pwmF_N2.start(0)
# pwmF_N4.start(0)

# center定義
center = 320
# 打開攝影機，圖像尺寸640*480（長*高），opencv存儲值爲480*640（行*列）
cap = cv2.VideoCapture(0)

joystick = pygame.joystick.Joystick(0)
joystick.init()

done = False
while not done:
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         sys.exit()

    event = pygame.event.get()
    
    if joystick.get_button(7):
        done = True

    # 取得影像
    ret, frame = cap.read()
    # print('ret:', ret)
    # print('frame:', frame)

    # 轉化爲灰度圖
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 大津法二值化
    retval, dst = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)
    # print('retval', retval)
    # print('dst', dst)

    # 儲存影像
    # filename2 = 'thres_' + datetime.now().strftime("%Y%m%d_%H%M%S") + '.jpg'
    # cv2.imwrite(filename2, dst)
    # print('frame', filename2)



    # 單看第437行的像素值
    color = dst[437 , 220:440]
    # 找到白色的像素點個數
    white_count = np.sum(color == 0)
    # 找到白色的像素點索引
    white_index = np.where(color == 0)


    # 防止white_count=0的報錯
    if white_count == 0:
        white_count = 1

    # 防呆
    if white_count - 1 >= white_index[0].size:
        print( datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'ERROR...STOP...')
        continue
    
    # 找到黑色像素的中心點位置
    # print('test', white_index[0][white_count - 1])
    center = (white_index[0][white_count - 1] + white_index[0][0]) / 2
    # print('center:',center)

    # 計算出center與標準中心點的偏移量
    direction = center - 100 


    print(direction)

    # 停止
    # if abs(direction) > 250:
    #     pwmB_N2.ChangeDutyCycle(0)
    #     pwmB_N4.ChangeDutyCycle(0)
    #     pwmF_N2.ChangeDutyCycle(0)
    #     pwmF_N4.ChangeDutyCycle(0)

    # 前進
    speed = 13
    rotate = 45

    #到達終點跳出迴圈
    if white_count > 180:
        pwmB_N2
        GPIO.output(F_N2,GPIO.LOW)
        pwmB_N4
        GPIO.output(F_N4,GPIO.LOW)
        pwmF_N2
        GPIO.output(B_N2,GPIO.LOW)
        pwmF_N4
        GPIO.output(B_N4,GPIO.LOW)  
        pwmB_N2.ChangeDutyCycle(speed)
        pwmB_N4.ChangeDutyCycle(speed)
        pwmF_N2.ChangeDutyCycle(speed)
        pwmF_N4.ChangeDutyCycle(speed) 
    
    elif direction < 25 and direction > -25:
        pwmB_N2
        GPIO.output(F_N2,GPIO.LOW)
        pwmB_N4
        GPIO.output(F_N4,GPIO.LOW)
        pwmF_N2
        GPIO.output(B_N2,GPIO.LOW)
        pwmF_N4
        GPIO.output(B_N4,GPIO.LOW)  
        pwmB_N2.ChangeDutyCycle(speed)
        pwmB_N4.ChangeDutyCycle(speed)
        pwmF_N2.ChangeDutyCycle(speed)
        pwmF_N4.ChangeDutyCycle(speed)  
    # 右轉      
    elif direction > 0:
        # 限制在70以內
        GPIO.output(F_N1,GPIO.LOW)
        GPIO.output(F_N2,GPIO.HIGH)
        pwmB_N4
        GPIO.output(F_N4,GPIO.LOW)
        GPIO.output(B_N1,GPIO.LOW)
        GPIO.output(B_N2,GPIO.HIGH)
        pwmF_N4
        GPIO.output(B_N4,GPIO.LOW)
        pwmB_N2.ChangeDutyCycle(rotate)
        pwmB_N4.ChangeDutyCycle(rotate +5)
        pwmF_N2.ChangeDutyCycle(rotate)
        pwmF_N4.ChangeDutyCycle(rotate+5)
        #pwmB_N2.ChangeDutyCycle(0)
        #pwmB_N4.ChangeDutyCycle(0)
        #pwmF_N2.ChangeDutyCycle(0)
        #pwmF_N4.ChangeDutyCycle(0)


    # 左轉
    elif direction < 0:
        pwmB_N2
        GPIO.output(F_N2,GPIO.LOW)
        GPIO.output(F_N3,GPIO.LOW)
        GPIO.output(F_N4,GPIO.HIGH)
        pwmF_N2
        GPIO.output(B_N2,GPIO.LOW)
        GPIO.output(B_N3,GPIO.LOW)
        GPIO.output(B_N4,GPIO.HIGH)
        pwmB_N2.ChangeDutyCycle(rotate)
        pwmB_N4.ChangeDutyCycle(rotate)
        pwmF_N2.ChangeDutyCycle(rotate)
        pwmF_N4.ChangeDutyCycle(rotate)

# 釋放清理
cap.release()
# cv2.destroyAllWindows()
pwmB_N2.stop()
pwmB_N4.stop()
pwmF_N2.stop()
pwmF_N4.stop()
GPIO.cleanup()






print('完成')


