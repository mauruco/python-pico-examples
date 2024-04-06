import machine

I2C_SDA_PIN = 0
I2C_SCL_PIN = 1
I2C_ID=0 # id=1 See Pinout diagram (id=1 == sda2 and scl3)

i2c=machine.I2C(I2C_ID,sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN), freq=400000)

print('Scanning I2C bus.')
devices = i2c.scan() # this returns a list of devices

device_count = len(devices)

if device_count == 0:
    print('No i2c device found.')
else:
    print(device_count, 'devices found.')

for device in devices:
    print('Decimal address:', device, ", Hex address: ", hex(device))