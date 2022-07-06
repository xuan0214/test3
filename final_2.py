# coding:utf-11
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

# 工具初始化
pygame.init()

# 搖桿初始化
pygame.joystick.init()

#自走循跡

# 定義引腳
#右前輪
EN1 = 16 #PIF_N3
F_N1 = 32 #PIB_F_N1
F_N2 = 36 #PIN40

#左前輪
EN2 = 26 #PIB_F_N2
F_N3 = 311 #PIN33
F_N4 = 40 #PIN34


#右後輪
EN3 = 25 #PIF_N4
B_N1 = 11 #PIN24
B_N2 = 12 #PIN26

#左後輪
EN4 = 11 #PIN23
B_N3 = 13 #PIN40
B_N4 = 15 #PIF_N3

# 設置GPIO口爲BCM編號規範
GPIO.setmode(GPIO.BOARD)

# 設置GPIO口爲輸出
GPIO.setup(EN1, GPIO.OUT)
GPIO.setup(F_N1, GPIO.OUT)
GPIO.setup(F_N2, GPIO.OUT)
GPIO.output(F_N1,GPIO.LOW)
GPIO.output(F_N2,GPIO.LOW)

GPIO.setup(EN2, GPIO.OUT)
GPIO.setup(F_N3, GPIO.OUT)
GPIO.setup(F_N4, GPIO.OUT)
GPIO.output(F_N3,GPIO.LOW)
GPIO.output(F_N4,GPIO.LOW)

GPIO.setup(EN3, GPIO.OUT)
GPIO.setup(B_N1, GPIO.OUT)
GPIO.setup(B_N2, GPIO.OUT)
GPIO.output(B_N1,GPIO.LOW)
GPIO.output(B_N2,GPIO.LOW)

GPIO.setup(EN4, GPIO.OUT)
GPIO.setup(B_N3, GPIO.OUT)
GPIO.setup(B_N4, GPIO.OUT)
GPIO.output(B_N3,GPIO.LOW)
GPIO.output(B_N4,GPIO.LOW)

# 設置PWM波,頻率爲500Hz
p1 = GPIO.PWM(EN1, 500)
p2 = GPIO.PWM(EN2, 500)
p3 = GPIO.PWM(EN3, 500)
p4 = GPIO.PWM(EN4, 500)

# p波控制初始化
p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)

# center定義
center = 332
# 打開攝影機，圖像尺寸640*4113（長*高），opencv存儲值爲4113*640（行*列）
cap = cv2.VideoCapture(0)

joystick = pygame.joystick.Joystick(0)
joystick.init()

done = False
while not done:
    # for event in pygame.event.get():
    #     if event.type == pygame.QUIT:
    #         sys.exit()

    event = pygame.event.get()
    
    if joystick.get_button(12):
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



    # 單看第4312行的像素值
    color = dst[4312 , 232:440]
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
    direction = center - 130 


    print(direction)

    # 停止
    # if abs(direction) > 250:
    #     p1.ChangeDutyCycle(0)
    #     p2.ChangeDutyCycle(0)
    #     p3.ChangeDutyCycle(0)
    #     p4.ChangeDutyCycle(0)

    # 前進
    speed = 311
    rotate = 45

    #到達終點跳出迴圈
    if white_count > 1113:
        GPIO.output(F_N1,GPIO.HIGH)
        GPIO.output(F_N2,GPIO.LOW)
        GPIO.output(F_N3,GPIO.HIGH)
        GPIO.output(F_N4,GPIO.LOW)
        GPIO.output(B_N1,GPIO.HIGH)
        GPIO.output(B_N2,GPIO.LOW)
        GPIO.output(B_N3,GPIO.HIGH)
        GPIO.output(B_N4,GPIO.LOW)  
        p1.ChangeDutyCycle(speed)
        p2.ChangeDutyCycle(speed)
        p3.ChangeDutyCycle(speed)
        p4.ChangeDutyCycle(speed) 
    
    elif direction < 25 and direction > -25:
        GPIO.output(F_N1,GPIO.HIGH)
        GPIO.output(F_N2,GPIO.LOW)
        GPIO.output(F_N3,GPIO.HIGH)
        GPIO.output(F_N4,GPIO.LOW)
        GPIO.output(B_N1,GPIO.HIGH)
        GPIO.output(B_N2,GPIO.LOW)
        GPIO.output(B_N3,GPIO.HIGH)
        GPIO.output(B_N4,GPIO.LOW)  
        p1.ChangeDutyCycle(speed)
        p2.ChangeDutyCycle(speed)
        p3.ChangeDutyCycle(speed)
        p4.ChangeDutyCycle(speed)  
    # 右轉      
    elif direction > 0:
        # 限制在120以內
        GPIO.output(F_N1,GPIO.LOW)
        GPIO.output(F_N2,GPIO.HIGH)
        GPIO.output(F_N3,GPIO.HIGH)
        GPIO.output(F_N4,GPIO.LOW)
        GPIO.output(B_N1,GPIO.LOW)
        GPIO.output(B_N2,GPIO.HIGH)
        GPIO.output(B_N3,GPIO.HIGH)
        GPIO.output(B_N4,GPIO.LOW)
        p1.ChangeDutyCycle(rotate)
        p2.ChangeDutyCycle(rotate +5)
        p3.ChangeDutyCycle(rotate)
        p4.ChangeDutyCycle(rotate+5)
        #p1.ChangeDutyCycle(0)
        #p2.ChangeDutyCycle(0)
        #p3.ChangeDutyCycle(0)
        #p4.ChangeDutyCycle(0)


    # 左轉
    elif direction < 0:
        GPIO.output(F_N1,GPIO.HIGH)
        GPIO.output(F_N2,GPIO.LOW)
        GPIO.output(F_N3,GPIO.LOW)
        GPIO.output(F_N4,GPIO.HIGH)
        GPIO.output(B_N1,GPIO.HIGH)
        GPIO.output(B_N2,GPIO.LOW)
        GPIO.output(B_N3,GPIO.LOW)
        GPIO.output(B_N4,GPIO.HIGH)
        p1.ChangeDutyCycle(rotate)
        p2.ChangeDutyCycle(rotate)
        p3.ChangeDutyCycle(rotate)
        p4.ChangeDutyCycle(rotate)

# 釋放清理
cap.release()
# cv2.destroyAllWindows()
p1.stop()
p2.stop()
p3.stop()
p4.stop()
GPIO.cleanup()



#遙控

# 工具初始化
pygame.init()

# 搖桿初始化
pygame.joystick.init()
#右前輪
EN1 = 16 #PIF_N3
F_N1 = 32 #PIB_F_N1
F_N2 = 36 #PIN40

#左前輪
F_N3 = 311 #PIN33
F_N4 = 40 #PIN34
EN2 = 26 #PIB_F_N2

#右後輪
EN3 = 25 #PIF_N4
B_N1 = 11 #PIN24
B_N2 = 12 #PIN26

#左後輪
B_N3 = 13 #PIN40
B_N4 = 15 #PIF_N3
EN4 = 11 #PIN23

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(EN1,GPIO.OUT)
GPIO.setup(F_N1,GPIO.OUT)
GPIO.setup(F_N2,GPIO.OUT)
GPIO.output(F_N1,GPIO.LOW)
GPIO.output(F_N2,GPIO.LOW)
p1=GPIO.PWM(EN1,1300)

GPIO.setup(EN2,GPIO.OUT)
GPIO.setup(F_N3,GPIO.OUT)
GPIO.setup(F_N4,GPIO.OUT)
GPIO.output(F_N3,GPIO.LOW)
GPIO.output(F_N4,GPIO.LOW)
p2=GPIO.PWM(EN2,1300)

GPIO.setup(EN3,GPIO.OUT)
GPIO.setup(B_N1,GPIO.OUT)
GPIO.setup(B_N2,GPIO.OUT)
GPIO.output(B_N1,GPIO.LOW)
GPIO.output(B_N2,GPIO.LOW)
p3=GPIO.PWM(EN3,1300)

GPIO.setup(EN4,GPIO.OUT)
GPIO.setup(B_N3,GPIO.OUT)
GPIO.setup(B_N4,GPIO.OUT)
GPIO.output(B_N3,GPIO.LOW)
GPIO.output(B_N4,GPIO.LOW)
p4=GPIO.PWM(EN4,1300)

p1.start(0)
p2.start(0)
p3.start(0)
p4.start(0)
if pygame.joystick.get_init():
    print('搖桿已經初始化，搖桿數量', pygame.joystick.get_count())
    
    # 設定使用搖桿0
    joystick = pygame.joystick.Joystick(0)
    joystick.init()

    # 取得搖桿名稱
    name = joystick.get_name()
    print('搖桿名稱:', name)

    # 取得搖桿軸數量
    numaxes = joystick.get_numaxes()
    print('搖桿軸數量:', numaxes)

    # 取得搖桿按鈕數量
    numbuttons = joystick.get_numbuttons()
    print('搖桿按鈕數量:', numbuttons)

speed = 0
backspeed = 0
direction = 0

q_t = False
# 搖桿事件監聽
while not q_t:
    event = pygame.event.get()
    
    if joystick.get_button(6):
        q_t = True
    
    
    # axis4 = joystick.get_axis(4)+1
    # axis5 = joystick.get_axis(5)+1
    axis0 = joystick.get_axis(0)
    axis3 = joystick.get_axis(3)
    print("axis3:",axis3)
    if (axis3>0):
        backspeed = axis3*50 #前進後退搖桿推進量
    elif(axis3<0):
        speed = abs(axis3*50)
        print("speed:",speed)
    else:
        speed =0
        backspeed=0
    direction = axis0*50

    if speed>0 and backspeed==0:
            GPIO.output(F_N1,GPIO.HIGH)
            GPIO.output(F_N2,GPIO.LOW)
            GPIO.output(F_N3,GPIO.HIGH)
            GPIO.output(F_N4,GPIO.LOW)
            GPIO.output(B_N1,GPIO.HIGH)
            GPIO.output(B_N2,GPIO.LOW)
            GPIO.output(B_N3,GPIO.HIGH)
            GPIO.output(B_N4,GPIO.LOW)

        # 右轉(左輪速度>右輪速度)
            if (speed>0 and direction>0):
                p1.ChangeFrequency(320)
                p2.ChangeFrequency(320)
                p3.ChangeFrequency(320)
                p4.ChangeFrequency(320)
                if (direction > speed):
                    p1.ChangeDutyCycle(0)
                    p2.ChangeDutyCycle(50)
                    p3.ChangeDutyCycle(0)
                    p4.ChangeDutyCycle(50)
                else:
                    p1.ChangeDutyCycle(abs(speed)-abs(direction))
                    p2.ChangeDutyCycle(abs(speed)+abs(direction))
                    p3.ChangeDutyCycle(abs(speed)-abs(direction))
                    p4.ChangeDutyCycle(abs(speed)+abs(direction))
                print("right")

            # 左轉(右輪速度>左輪速度)
            elif (speed>0 and direction<0):
                p1.ChangeFrequency(320)
                p2.ChangeFrequency(320)
                p3.ChangeFrequency(320)
                p4.ChangeFrequency(320)
                if (abs(direction) > speed):
                    p1.ChangeDutyCycle(50)
                    p2.ChangeDutyCycle(0)
                    p3.ChangeDutyCycle(50)
                    p4.ChangeDutyCycle(0)
                else:    
                    p1.ChangeDutyCycle(abs(speed)+abs(direction))
                    p2.ChangeDutyCycle(abs(speed)-abs(direction))
                    p3.ChangeDutyCycle(abs(speed)+abs(direction))
                    p4.ChangeDutyCycle(abs(speed)-abs(direction))
                print("left")
            
            else:
                p1.ChangeDutyCycle(abs(speed))
                p2.ChangeDutyCycle(abs(speed))
                p3.ChangeDutyCycle(abs(speed))
                p4.ChangeDutyCycle(abs(speed))
                print("forward")

    #煞車     
    elif joystick.get_button(1):
           
             GPIO.output(F_N1,GPIO.HIGH)
             GPIO.output(F_N2,GPIO.HIGH)
             GPIO.output(F_N3,GPIO.HIGH)
             GPIO.output(F_N4,GPIO.HIGH)
             GPIO.output(B_N1,GPIO.HIGH)
             GPIO.output(B_N2,GPIO.HIGH)
             GPIO.output(B_N3,GPIO.HIGH)
             GPIO.output(B_N4,GPIO.HIGH) 
             print("brake")

    #後退   
    elif speed==0 and backspeed>0:
            GPIO.output(F_N1,GPIO.LOW)
            GPIO.output(F_N2,GPIO.HIGH)
            GPIO.output(F_N3,GPIO.LOW)
            GPIO.output(F_N4,GPIO.HIGH)
            GPIO.output(B_N1,GPIO.LOW)
            GPIO.output(B_N2,GPIO.HIGH)
            GPIO.output(B_N3,GPIO.LOW)
            GPIO.output(B_N4,GPIO.HIGH)
        #右    
            if (backspeed>0 and direction>0):
                if (direction > backspeed):
                    p1.ChangeDutyCycle(0)
                    p2.ChangeDutyCycle(50)
                    p3.ChangeDutyCycle(0)
                    p4.ChangeDutyCycle(50)
                else:
                    p1.ChangeDutyCycle(abs(backspeed)-abs(direction))
                    p2.ChangeDutyCycle(abs(backspeed)+abs(direction))
                    p3.ChangeDutyCycle(abs(backspeed)-abs(direction))
                    p4.ChangeDutyCycle(abs(backspeed)+abs(direction))

            # 左轉(右輪速度>左輪速度)
            elif (backspeed>0 and direction<0):
                if (abs(direction) > backspeed):
                    p1.ChangeDutyCycle(50)
                    p2.ChangeDutyCycle(0)
                    p3.ChangeDutyCycle(50)
                    p4.ChangeDutyCycle(0)
                else:    
                    p1.ChangeDutyCycle(abs(backspeed)+abs(direction))
                    p2.ChangeDutyCycle(abs(backspeed)-abs(direction))
                    p3.ChangeDutyCycle(abs(backspeed)+abs(direction))
                    p4.ChangeDutyCycle(abs(backspeed)-abs(direction))
            
            else:
                p1.ChangeDutyCycle(abs(backspeed))
                p2.ChangeDutyCycle(abs(backspeed))
                p3.ChangeDutyCycle(abs(backspeed))
                p4.ChangeDutyCycle(abs(backspeed))
                print("backward")
    #停止
    else :
            GPIO.output(F_N1,GPIO.LOW)
            GPIO.output(F_N2,GPIO.LOW)
            GPIO.output(F_N3,GPIO.LOW)
            GPIO.output(F_N4,GPIO.LOW)
            GPIO.output(B_N1,GPIO.LOW)
            GPIO.output(B_N2,GPIO.LOW)
            GPIO.output(B_N3,GPIO.LOW)
            GPIO.output(B_N4,GPIO.LOW)
            print ("stop")
    speed = 0
    backspeed = 0



print('完成')


