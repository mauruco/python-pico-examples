from time import sleep

### Developed by Mauro Brizida mauruco@gmail.com
# Tutorials I used to develop this code
# https://docs.micropython.org/en/latest/library/machine.I2C.html


### IMPORTANT Do not forget to calibrate the MPU6050
# Calibrate Z
# calibrate_accel()
# Pitch Up 90 degrees, calibrate X
# calibrate_accel()
# Roll Right 90 degrees, calibrate Y
# calibrate_accel()
# Gyro
# calibrate_gyro()

### GOOD TO KNOW
## PS4/PS3
# Accelerometer g-force measurement range
# DS4 (programmable) +/- 2 g, +/- 4 g, +/- 8 g, +/- 16 g
# DS3 +/- 2 g
# Gyroscope angular rate measurement range
# DS4 (programmable) +/- 125°/s, +/- 250°/s, +/- 500°/s, +/- 1000°/s, +/- 2000°/s
# DS3 +/- 100°/s

## joycon
# Sensitivity	Noise level range
# +/- 2G	328 * 2.5 = 2050
# +/- 4G	164 * 2.5 = 410
# +/- 8G (default)	82 * 2.5 = 205
# +/- 16G	No official value
# Gyroscope:
# Sensitivity	Noise level range
# +/- 250dps	236 * 2.5 = 590
# +/- 500dps	118 * 2.5 = 295
# +/- 1000dps	59 * 2.5 = 147
# +/- 2000dps (default)	30 * 2.5 = 75

## Euler angles convention
# Pitch: Rotation around the X-axis. + is nose up, - is nose down.
# Roll: Rotation around the Y-axis. + is right wing down, - is left wing down.
# Yaw: Rotation around the Z-axis. + is counterclockwise, - is clockwise.

class MPU6050:
  def __init__(self, mpuAddr, i2c, gyro_sensitive_range = 2, accel_sensitive_range = 2):
    self.mpuAddr = mpuAddr
    self.i2c = i2c
    ## wake device
    # Bit 7: DEVICE_RESET - When the bit is set to '1', the MPU-6050 is reset to factory default settings.
    # Bit 6: SLEEP - When the bit is set to '1', the MPU-6050 enters sleep mode.
    # Bit 5: CYCLE - When the bit is set to '1', the MPU-6050 enters cycle mode.
    # Bit 4: TEMP_DIS - When the bit is set to '1', the temperature sensor is disabled.
    # Bits 3 and 2: CLKSEL[1:0] - Clock source selector.
    # Bits 1 and 0: Reserved.
    i2c.writeto_mem(mpuAddr, 0x6B, bytes([0])) # write 0 to register 0x6B
    # wait for the device to wake up
    sleep(0.2)

    ## GOOD TO KNOW
    # Once DMP is enabled, the acc range must be +-4g and gyro +-2000 dps, required by the DMP
    ## disable DMP
    # MPU6050 register
    # Read the current value of the USER_CTRL register
    user_ctrl = i2c.readfrom_mem(mpuAddr, 0x6A, 1)[0]

    # Clear the DMP_EN bit (bit 7) to disable DMP
    user_ctrl &= ~0x80

    # Write the new value back to the USER_CTRL register
    i2c.writeto_mem(mpuAddr, 0x6A, bytes([user_ctrl]))

    ## low pass filter
    self.set_low_pass_filter(5)

    ## sensitive range
    self.gyro_sensitive_range = gyro_sensitive_range
    self.gyro_sensitive = [131, 65.5, 32.8, 16.4]
    self.accel_sensitive_range = accel_sensitive_range
    self.accel_sensitive = [16384, 8192, 4096, 2048]
    self.set_sensitive_range(self.gyro_sensitive_range, self.accel_sensitive_range)

  ## combine register into 16 bits
  @micropython.viper
  def combine_h_l(self, high: uint, low: uint) -> int:
    val =  int((high << 8) | low)
    # check if sign bit is set a two's complement must be applied
    if high & 0x80:
        val = val - 65536 # equivalent to temp_val = -((temp_val ^ 0xFFFF) + 1)
    return val

  ## read chip id
  def read_chip_id(self):
    chip_id = self.i2c.readfrom_mem(0x68, 0x75, 1)
    chip_id_int = int.from_bytes(chip_id, 'big') # Convert bytes to int

  ## set low pass filter
  def set_low_pass_filter(self, value):
    ### Maybe try ou low pass filter
    # MPU6050 registers
    # 000 = Accel: 260Hz, Gyro: 256Hz
    # 001 = Accel: 184Hz, Gyro: 188Hz
    # 010 = Accel: 94Hz, Gyro: 98Hz
    # 011 = Accel: 44Hz, Gyro: 42Hz
    # 100 = Accel: 21Hz, Gyro: 20Hz
    # 101 = Accel: 10Hz, Gyro: 10Hz
    # 110 = Accel: 5Hz, Gyro: 5Hz
    # 111 = Reserved
    # Set DLPF_CFG to 3 (Accel: 10Hz, Gyro: 10Hz)
    self.i2c.writeto_mem(self.mpuAddr, 0x1A, bytes([value]))

  ## set sensitive range
  def set_sensitive_range(self, gyro_sensitive_range, accel_sensitive_range):
    #### IMPORTANT These registers expect a value where the relevant bits for sensitivity are bits 4 and 3
    ### set gyroscope range sensitivity
    # 0 0x00 = +/- 250 °/s 131 LSB/°/s Default value
    # 1 0x01 = +/- 500 °/s 65.5 LSB/°/s
    # 2 0x10 = +/- 1000 °/s 32.8 LSB/°/s
    # 3 0x11 = +/- 2000 °/s 16.4 LSB/°/s
    self.i2c.writeto_mem(0x68, 0x1B, bytes([gyro_sensitive_range << 3]))


    ### set accelerometer range sensitivity
    # 0 0x00 = +/- 2g 16384 LSB/g Default value
    # 1 0x01 = +/- 4g 8192 LSB/g
    # 2 0x10 = +/- 8g 4096 LSB/g
    # 3 0x11 = +/- 16g 2048 LSB/g
    self.i2c.writeto_mem(0x68, 0x1C, bytes([accel_sensitive_range << 3]))

  ## read raw data
  def read_accel_raw(self):
    # Read acceleration data from MPU6050
    accel_x_h = self.i2c.readfrom_mem(0x68, 0x3B, 1)[0]
    accel_x_l = self.i2c.readfrom_mem(0x68, 0x3C, 1)[0]
    accel_y_h = self.i2c.readfrom_mem(0x68, 0x3D, 1)[0]
    accel_y_l = self.i2c.readfrom_mem(0x68, 0x3E, 1)[0]
    accel_z_h = self.i2c.readfrom_mem(0x68, 0x3F, 1)[0]
    accel_z_l = self.i2c.readfrom_mem(0x68, 0x40, 1)[0]

    # Combine high and low bytes
    accel_x_val = self.combine_h_l(accel_x_h, accel_x_l) / self.accel_sensitive[self.accel_sensitive_range] # convert to g
    accel_y_val = self.combine_h_l(accel_y_h, accel_y_l) / self.accel_sensitive[self.accel_sensitive_range]
    accel_z_val = self.combine_h_l(accel_z_h, accel_z_l) / self.accel_sensitive[self.accel_sensitive_range]

    return accel_x_val, accel_y_val, accel_z_val

  ## read raw data
  def read_gyro_raw(self):
    # Read gyroscope data from MPU6050
    gyro_x_h = self.i2c.readfrom_mem(0x68, 0x43, 1)[0]
    gyro_x_l = self.i2c.readfrom_mem(0x68, 0x44, 1)[0]
    gyro_y_h = self.i2c.readfrom_mem(0x68, 0x45, 1)[0]
    gyro_y_l = self.i2c.readfrom_mem(0x68, 0x46, 1)[0]
    gyro_z_h = self.i2c.readfrom_mem(0x68, 0x47, 1)[0]
    gyro_z_l = self.i2c.readfrom_mem(0x68, 0x48, 1)[0]

    # Combine high and low bytes
    gyro_x_val = self.combine_h_l(gyro_x_h, gyro_x_l) / self.gyro_sensitive[self.gyro_sensitive_range] # convert to degrees per second
    gyro_y_val = self.combine_h_l(gyro_y_h, gyro_y_l) / self.gyro_sensitive[self.gyro_sensitive_range]
    gyro_z_val = self.combine_h_l(gyro_z_h, gyro_z_l) / self.gyro_sensitive[self.gyro_sensitive_range]

    return gyro_x_val, gyro_y_val, gyro_z_val

  ## read temperature   
  def read_temp_celsius(self):
    # reading 2 bytes at once
    temp = self.i2c.readfrom_mem(0x68, 0x41, 2)
    # Convert to 16-bit signed values
    temp_val = int.from_bytes(temp, 'big')
    if temp_val & 0x8000:  # if sign bit is set, compute negative value
        temp_val -= 65536
    # Convert raw value to Celsius
    temp_val = temp_val / 340.0 + 36.53
    return temp_val
  
  ## calibrate the gyroscope
  def calibrate_gyro(self):
    # Calibrate the gyroscope
    # The gyroscope is calibrated by reading the average value of the gyroscope data when the sensor is at rest
    # Wait for MPU to Settle
    gxTotal, gyTotal, gzTotal = 0, 0, 0
    for y in range(10):
      for i in range(1000):
        gx, gy, gz = self.read_gyro_raw()
        gxTotal += gx
        gyTotal += gy
        gzTotal += gz
        sleep(0.01)

    return {
      'gx': gxTotal / 10000,
      'gy': gyTotal / 10000,
      'gz': gzTotal / 10000
    }

  ## calibrate the accelerometer
  def calibrate_accel(self):
    # Rotate the sensor around all axes 90 degrees to calibrate the accelerometer
    # x, y, and should have +/- 1g of acceleration
    axTotal, ayTotal, azTotal = 0, 0, 0
    for y in range(10):
      for i in range(1000):
        ax, ay, az = self.read_accel_raw()
        axTotal += ax
        ayTotal += ay
        azTotal += az
        sleep(0.01)

    axTotal = axTotal / 10000
    ayTotal = ayTotal / 10000
    azTotal = azTotal / 10000

    axAbs = abs(axTotal)
    ayAbs = abs(ayTotal)
    azAbs = abs(azTotal)

    # presume az is the closest to 1g
    useAccel = 'az'
    total = azAbs
    totalOrignal = azTotal
    offset = 0

    if axAbs > ayAbs and axAbs > azAbs:
      useAccel = 'ax'
      total = axAbs
      totalOrignal = axTotal
    if ayAbs > axAbs and ayAbs > azAbs:
      useAccel = 'ay'
      total = ayAbs
      totalOrignal = ayTotal

    # lower then -1 or bigger then 1
    if total > 1:
      offset = 1 - total
      if totalOrignal > 0:
        offset = -offset
    # bigger then -1 and lower then 1
    else:
      offset = total - 1
      if totalOrignal < 0:
        offset = -offset

    return {
      useAccel: offset,
    }

  ## get correct accelerometer and gyroscope values
  def get_acc_gyro(self, offsetAX, offsetAY, offsetAZ, offsetGX, offsetGY, offsetGZ):
    ax, ay, az = self.read_accel_raw()
    gx, gy, gz = self.read_gyro_raw()
    ax -= offsetAX
    ay -= offsetAY
    az -= offsetAZ
    gx -= offsetGX
    gy -= offsetGY
    gz -= offsetGZ
    return ax, ay, az, gx, gy, gz

### INT PIN on the MPU6050
# # INT pin is used to indicate that data is ready to read
# MPU6050_INT_ENABLE = 0x38 # 0x38 is the address of the register to enable the interrupt
# i2c.writeto_mem(self.mpuAddr, MPU6050_INT_ENABLE, bytes([1])) # write 1 to register 0x38
# mpuIntPin = Pin(4, Pin.IN, Pin.PULL_UP) # set pin 4 as input
# mpuIntPin.irq(trigger=Pin.IRQ_FALLING, handler=lambda p: print("Data ready to read")) # set interrupt handler
# mpuIntPin.irq(trigger=Pin.IRQ_FALLING, handler=read_temp) # set interrupt handler