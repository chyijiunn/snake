from machine import Pin, I2C,PWM
from ssd1306 import SSD1306_I2C
from time import sleep
import _thread

oled = SSD1306_I2C(128, 64, I2C(0,sda=Pin(20), scl=Pin(21), freq=40000))
buttonR = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)
buttonL = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)
buzzer = PWM(Pin(12))
buzzer.freq(500)

oled.fill(0)
x = 64
y = 32
direction = 0
path =[]
def button_thread():
    global direction
    while True:
        if buttonR.value() == 0:direction = direction + 1
        if buttonL.value() == 0:direction = direction - 1
        sleep(0.1)

def fail():
    buzzer.duty_u16(1000)
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
    buzzer.duty_u16(0)

_thread.start_new_thread(button_thread, ())

while True:
    if x > 128: x =0
    if x <0: x = 128
    if y > 64 : y =0
    if y <0 : y = 64
    
    if direction % 4 == 0:x +=1
    if direction % 4 == 1:y +=1
    if direction % 4 == 2:x -=1
    if direction % 4 == 3:y -=1
    
    oled.pixel(x,y,1)
    
    if buttonR.value() == 0 and buttonL.value() == 0:break
    
    oled.show()
    
    if [x,y] in path:
        fail()
        break
    path.append([x,y])
