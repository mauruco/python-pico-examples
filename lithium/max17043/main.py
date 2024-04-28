# How to use the MAX17043 class:
import machine
from __init__ import MAX17043

I2C_SDA_PIN = 14
I2C_SCL_PIN = 15
I2C_ID=1 # id=1 See Pinout diagram (id=1 == sda2 and scl3)

max17043 = MAX17043(machine.I2C(I2C_ID, sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN)))

# print version
print('IC Version:', max17043.read_ic_version())

# print battery percentage
print('Battery Percentage:', max17043.read_battery_percentage())

# print battery voltage
print('Battery Voltage:', max17043.read_battery_voltage())