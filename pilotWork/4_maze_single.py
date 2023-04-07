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

#以下設定出發點和方向(0~3 = 右下左上)
x = 50
y = 37
direction = 0

#以下設定終點
goal = [[79,36],[79,37],[79,38]]

path =[]

def maze():
    oled.fill(0)
    data = open('data/maze/01','r')
    for line in data:
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

def scoreshow():
    score = len(path)-251#減掉(迷宮block數+1)
    oled.text('score '+str(score),40,55)
        
    data = open('data/record/record_mazeS')
    top = int(data.readline())
    if score > top:
        data = open('data/record/record_mazeS','w')
        data.write(str(score))
        top = score
        
    oled.text('TOP '+str(top),40,0)
    data.close()
    oled.show()
    
def buzz():
    buzzer.duty_u16(1000)
    sleep(1)
    buzzer.duty_u16(0)

    
maze()
_thread.start_new_thread(button_thread, ())

while True: 
    if direction % 4 == 0:x = x + 1
    if direction % 4 == 1:y = y + 1
    if direction % 4 == 2:x = x - 1
    if direction % 4 == 3:y = y - 1
    
    oled.pixel(x,y,1)
    oled.show()
    
    if [x,y] in path:
        buzz()
        scoreshow()
        break
    
    if [x,y] in goal:
        buzz()
        oled.text('Pass!',30,55)
        oled.show()
        break
    path.append([x,y])
