from machine import Pin, I2C,PWM
from ssd1306 import SSD1306_I2C
from time import sleep
import _thread ,random

buzzer = PWM(Pin(12))
buzzer.freq(500)
i2c=I2C(0,sda=Pin(20), scl=Pin(21), freq=40000)
oled = SSD1306_I2C(128, 64, i2c)
buttonU = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_UP)#press = 0 , unpress = 1
buttonD = machine.Pin(0, machine.Pin.IN, machine.Pin.PULL_UP)
buttonL = machine.Pin(2, machine.Pin.IN, machine.Pin.PULL_UP)
buttonR = machine.Pin(3, machine.Pin.IN, machine.Pin.PULL_UP)
buttonA = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_UP)
buttonB = machine.Pin(5, machine.Pin.IN, machine.Pin.PULL_UP)
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
        if buttonU.value() == 0 : direction = 0
        elif buttonD.value() == 0 : direction = 1
        elif buttonL.value() == 0 : direction = 2
        elif buttonR.value() == 0: direction = 3

        sleep(0.01)
        
def buzz():
    buzzer.duty_u16(1000)
    sleep(1)
    buzzer.duty_u16(0)

def scoreshow():
    score = len(path)-1
    oled.text('score '+str(score),40,55)
        
    data = open('data/maze/00_r')
    top = int(data.readline())
    if score > top:
        data = open('data/maze/00_r','w')
        data.write(str(score))
        top = score
        
    oled.text('TOP '+str(top),0,0)
    data.close()
    oled.show()
    
_thread.start_new_thread(button_thread, ())

while True:
    oled.pixel(x,y,1)
    oled.show()
    
    if  direction == 0  : y -= 1
    elif direction == 1: y += 1
    elif direction == 2 : x -= 1 
    elif direction == 3: x += 1
    
    if x > 128: x =0
    if x <0: x = 128
    if y > 64 : y =0
    if y <0 : y = 64
    
    if [x,y] in path:
        buzz()
        draw()
        scoreshow()
        break

    path.append([x,y])
    if buttonA.value() == 0 and buttonB.value() == 0:break