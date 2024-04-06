### OLED 0.96" 128x64 I2C Display
https://docs.micropython.org/en/latest/esp8266/tutorial/ssd1306.html  
https://github.com/stlehmann/micropython-ssd1306/blob/master/ssd1306.py  


## PINOUT
```txt
                                         ---usb---
UART0 TX - I2C0 SDA - SPI0 RX  - GP0  1  |o     o| 40  VBUS
UART0 RX - I2C0 SCL - SPI0 CSn - GP1  2  |o     o| 39  VSYS
                                 GND  3  |o     o| 38  GND
           I2C1 SDA - SPI0 SCK - GP2  4  |o     o| 37  3V3_EN
           I2C1 SCL - SPI0 TX  - GP3  5  |o     o| 36  3V3(OUT)
UART1 TX - I2C0 SDA - SPI0 RX  - GP4  6  |o     o| 35         ADC_VREF
UART1 RX - I2C0 SCL - SPI0 CSn - GP5  7  |o     o| 34  GP28   ADC2
                                 GND  8  |o     o| 33  GND    AGND
           I2C1 SDA - SPI0 SCK - GP6  9  |o     o| 32  GP27   ADC1     - I2C1 SCL
           I2C1 SCL - SPI0 TX  - GP7  10 |o     o| 31  GP26   ADC0     - I2C1 SDA
UART1 TX - I2C0 SDA - SPI1 RX  - GP8  11 |o     o| 30  RUN
UART1 RX - I2C0 SCL - SPI1 CSn - GP9  12 |o     o| 29  GP22
                                 GND  13 |o     o| 28  GND
           I2C1 SDA - SPI1 SCK - GP10 14 |o     o| 27  GP21            - I2C0 SCL
           I2C1 SCL - SPI1 TX  - GP11 15 |o     o| 26  GP20            - I2C0 SDA
UART0 TX - I2C0 SDA - SPI1 RX  - GP12 16 |o     o| 25  GP19 - SPI0 TX  - I2C1 SCL
UART0 RX - I2C0 SCL - SPI1 CSn - GP13 17 |o     o| 24  GP18 - SPI0 SCK - I2C1 SDA
                                 GND  18 |o     o| 23  GND
           I2C1 SDA - SPI1 SCK - GP14 19 |o     o| 22  GP17 - SPI0 CSn - I2C0 SCL - UART0 RX
           I2C1 SCL - SPI1 TX  - GP15 20 |o     o| 21  GP16 - SPI0 RX  - I2C0 SDA - UART0 TX
                                         ---------
```