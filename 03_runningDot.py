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
#path =[]
def button_thread():
    global direction
    while True:
        if buttonR.value() == 0:direction = direction + 1
        if buttonL.value() == 0:direction = direction - 1
        sleep(0.1)
    
_thread.start_new_thread(button_thread, ())

while True:
    #OLED 不刷新，螢幕點不消失
    oled.fill(0)
    
    if direction % 4 == 0:x +=1
    if direction % 4 == 1:y +=1
    #另外兩個怎麼設計呢？
    
    #到邊緣後要能跳到螢幕另一側
    oled.pixel(x,y,1)
    
    if buttonR.value() == 0 and buttonL.value() == 0:break
    oled.show()
    #path.append([x,y])