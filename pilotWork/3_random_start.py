from machine import Pin, I2C,PWM
from ssd1306 import SSD1306_I2C
from time import sleep
import _thread ,random

buzzer = PWM(Pin(7))
buzzer.freq(500)
i2c=I2C(0,sda=Pin(20), scl=Pin(21), freq=40000)
oled = SSD1306_I2C(128, 64, i2c)
buttonR = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)#press = 0 , unpress = 1
buttonL = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

oled.fill(0)

x = random.randint(0,127)
y = random.randint(0,63)
direction = random.randint(0,4)
path =[]

def draw():
    oled.fill(0)
    data = open('data/pics/boom','r')
    for line in data:
        a = line.split()
        for i in range(len(a)):
            xAxis = int(a[i].split(',')[0])
            yAxis = int(a[i].split(',')[1])
            oled.pixel(xAxis,yAxis,1)
    data.close()
    oled.show()

def button_thread():
    global direction
    while True:
        if buttonR.value() == 0:direction = direction + 1
        if buttonL.value() == 0:direction = direction - 1
        if buttonR.value() == 0 and buttonL.value() == 0:break
        sleep(0.15)
        
def buzz():
    buzzer.duty_u16(1000)
    sleep(1)
    buzzer.duty_u16(0)

def scoreshow():
    score = len(path)-1
    oled.text('score '+str(score),40,55)
        
    data = open('data/record/record')
    top = int(data.readline())
    if score > top:
        data = open('data/record/record','w')
        data.write(str(score))
        top = score
        
    oled.text('TOP '+str(top),0,0)
    data.close()
    oled.show()
    
_thread.start_new_thread(button_thread, ())

while True: 
    if x > 128: x =0
    if x <0: x = 128
    if y > 64 : y =0
    if y <0 : y = 64
    if direction % 4 == 0:x = x + 1
    if direction % 4 == 1:y = y + 1
    if direction % 4 == 2:x = x - 1
    if direction % 4 == 3:y = y - 1
    if buttonR.value() == 0 and buttonL.value() == 0:break
    
    oled.pixel(x,y,1)
    oled.show()
    
    if [x,y] in path:
        buzz()
        draw()
        scoreshow()
        break

    path.append([x,y])