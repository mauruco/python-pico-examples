import machine
import utime as time
import __init__ as ssd1306

# https://docs.micropython.org/en/v1.22.0/esp8266/tutorial/ssd1306.html
# https://github.com/micropython/micropython-lib/blob/58f8bec54d5b3b959247b73a6e8f28e8493bd30b/micropython/drivers/display/ssd1306/ssd1306.py


I2C_SDA_PIN = 14
I2C_SCL_PIN = 15
I2C_ID=1 # id=1 See Pinout diagram (id=1 == sda2 and scl3)

i2c=machine.I2C(I2C_ID,sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN))

# 0.42 inch OLED display
oled_width = 72
oled_height = 40
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)

# clear, Preenche o buffer de imagem com 0s (pixels desligados)
oled.fill(0)

# write text
oled.text('1234567891011', 0, 0)

# fill
oled.show()

