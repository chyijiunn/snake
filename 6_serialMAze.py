from machine import Pin, I2C,PWM 
from ssd1306 import SSD1306_I2C
from time import sleep
import _thread ,random,sys

buzzer = PWM(Pin(12))
buzzer.freq(500)
i2c=I2C(0,sda=Pin(20), scl=Pin(21), freq=40000)
oled = SSD1306_I2C(128, 64, i2c)
buttonR = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)#press = 0 , unpress = 1
buttonL = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)

#MazeData

goal = [ ]
path =[ ]
score =-1

def maze(fileSerial):
    global direction
    global x , y
    mazeName = '{:0>2}'.format(fileSerial)#格式化、前面補零
    oled.fill(0)
    data = open('data/maze/'+mazeName,'r')
    head = data.readline().split(',')   
    num = len(head)-1                   
    b = head[:num]                      
    
    direction = int(b[0])          
    x = int(b[1])                   
    y = int(b[2])
    for i in range(int((num-3)/2)):   
        goal.append([int(b[2*i+3]),int(b[2*i+4])])

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

def scoreshow(score,mazeName):
    buzzer.duty_u16(1000)
    sleep(1)
    buzzer.duty_u16(0)
    
    oled.fill_rect(0, 55, 127, 63, 1)
    oled.text('score '+str(score),35,55,0)
    
    mazeName = '{:0>2}'.format(fileSerial)#格式化、前面補零
    data = open('data/maze/'+mazeName+'_r')
    top = int(data.readline())
    
    if score > top:
        data = open('data/maze/'+mazeName+'_r','w')
        data.write(str(score))
        top = score
        
    oled.fill_rect(0, 0, 127, 7, 1)
    oled.text('TOP '+str(top),40,0,0)
    data.close()
    oled.show()
    
_thread.start_new_thread(button_thread, ())

for fileSerial in range(8):
    maze(fileSerial)
    while True:
        if direction % 4 == 0:x += 1
        if direction % 4 == 1:y +=  1
        if direction % 4 == 2:x -= 1
        if direction % 4 == 3:y -= 1
        
        oled.pixel(x,y,1)
        score = score + 1
        oled.show()
            
        if [x,y] in path:
            scoreshow(score,fileSerial)
            sys.exit()
        path.append([x,y])
            
        if not ([x,y] in goal) : continue
        oled.text('Pass!',40,55)
        oled.show()
        del path[:]#path清空
        #oled.fill(0)
        #oled.text('>>',20,30)
        for pixel in range(10):
            oled.scroll(10,0)
            oled.show()
        
        break