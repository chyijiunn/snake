from machine import Pin, I2C,PWM
from ssd1306 import SSD1306_I2C
from time import sleep
import _thread ,random

buzzer = PWM(Pin(7))
buzzer.freq(500)
i2c=I2C(0,sda=Pin(20), scl=Pin(21), freq=40000)
oled = SSD1306_I2C(128, 64, i2c)
buttonR = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)#press = 0 , unpress = 1
buttonL = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

oled.fill(0)

mazedataname = 'maze_01'                #MazeFileName
#出發點，起始分數，出發點不算分數，故為 -1
goal = [ ]
path =[ ]
score =-1

def maze():
    global direction
    global x , y
    oled.fill(0)

    data = open('data/maze/'+mazedataname,'r')
    head = data.readline().split(',')   #第一行 head 資料 str -> list
    num = len(head)-1                   #計算list內資料量，
    b = head[:num]                      #後皆換行符號，捨棄
    
    direction = int(b[0])           #第 1 碼:方向(0~3 = 右下左上)
    x = int(b[1])                      # 2~3 :start x ,y
    y = int(b[2])
    for i in range(int((num-3)/2)):     # 去掉 b[0]~b[2]，剩下皆為 goal point，計算個數
        goal.append([b[2*i+3],b[2*i+4]])#加入空白 goal

    #以下處理迷宮座標資料，使用 readlines 讀取剩餘資料
    mazelist = data.readlines()
    for line in mazelist:
        a = line.split()
        for i in range(len(a)):
            xAxis = int(a[i].split(',')[0])
            yAxis = int(a[i].split(',')[1])
            oled.pixel(xAxis,yAxis,1)
            path.append([xAxis,yAxis])
    data.close()
    oled.show()

def button_thread():
    global direction
    while True:
        if buttonR.value() == 0:direction = direction + 1
        if buttonL.value() == 0:direction = direction - 1
        if buttonR.value() == 0 and buttonL.value() == 0:break
        sleep(0.15) 

def scoreshow(score):
    oled.fill_rect(0, 55, 127, 63, 1)
    oled.text('score '+str(score),35,55,0)
    data = open('data/maze/'+mazedataname+'_r')
    top = int(data.readline())
    
    if score > top:
        data = open('data/maze/'+mazedataname+'_r','w')
        data.write(str(score))
        top = score
        
    oled.fill_rect(0, 0, 127, 7, 1)
    oled.text('TOP '+str(top),40,0,0)
    data.close()
    oled.show()
    
def buzz():
    buzzer.duty_u16(1000)
    sleep(0.1)
    buzzer.duty_u16(0)
    
maze()
_thread.start_new_thread(button_thread, ())

while True:
    
    if direction % 4 == 0:x += 1
    if direction % 4 == 1:y +=  1
    if direction % 4 == 2:x -= 1
    if direction % 4 == 3:y -= 1
   
    oled.pixel(x,y,1)
    score = score + 1
    oled.show()
    
    if [x,y] in path:
        buzz()
        scoreshow(score)
        break
    
    if [x,y] in goal:
        buzz()
        oled.text('Pass!',30,55)
        oled.show()
        break
    path.append([x,y])
