from machine import Pin, I2C,PWM
from ssd1306 import SSD1306_I2C#with package micropython-ssd1306
import time

i2c=I2C(0,sda=Pin(20), scl=Pin(21), freq=40000)
oled = SSD1306_I2C(128, 64, i2c)
buzzer = PWM(Pin(12))
buzzer.freq(500)
buttonR = machine.Pin(16, machine.Pin.IN, machine.Pin.PULL_UP)#press = 0 , unpress = 1
buttonL = machine.Pin(15, machine.Pin.IN, machine.Pin.PULL_UP)

oled.fill(0)
oled.text('hello',0,0)
oled.text('hello2',0,10)#寫文字於(0,10)
oled.line(0,15,127,15,1)#畫條線(x0,y0,x1,y1,1)
oled.pixel(64,30,1)#放一個點於64,30
oled.show()

print(buttonR.value(),buttonL.value())

buzzer.duty_u16(1000)
time.sleep(1)
buzzer.duty_u16(0)