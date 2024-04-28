import utime
import cmds
import acc
import gyr

## to signed
# data = ustruct.unpack("<h", data)[0]
## to unsigned
# = ustruct.pack('h', data)

class BMI160:
    def __init__(self, i2c, gyro_sensitive_range = gyr.GYR_2000, accel_sensitive_range = acc.ACC_8G, gyro_rate = gyr.GYR_RATE_1600, accel_rate = acc.ACC_RATE_1600):
      self.i2c = i2c

      # check chip id
      chip_id = i2c.readfrom_mem(0x69, 0x00, 1)
      chip_id_int = int.from_bytes(chip_id, 'big') # Convert bytes to int
      if chip_id_int != 0xD1:
        raise ValueError("Invalid chip id: %x" % chip_id_int)
      
      print("BMI160 initialized")

      # reset to default state
      self.cmd(cmds.SOFT_RESET)
      utime.sleep(0.1)

      # force  I2C commons mode
      self.i2c.readfrom_mem(0x69, 0x7F, 1)
      utime.sleep(0.1)

      # set gyro rate
      self.i2c.writeto_mem(0x69, 0x42, bytearray([gyro_rate]))
      utime.sleep(0.1)

      # set acc rate
      self.i2c.writeto_mem(0x69, 0x40, bytearray([accel_rate]))
      utime.sleep(0.1)

      # set gyro range
      self.i2c.writeto_mem(0x69, 0x43, bytearray([gyro_sensitive_range]))
      utime.sleep(0.1)

      # set acc range
      self.i2c.writeto_mem(0x69, 0x41, bytearray([accel_sensitive_range]))
      utime.sleep(0.1)

      # scale factor gyro
      self.GYR_SCALE_FACTOR = gyr.GYR_SCALE_FACTORS[gyro_sensitive_range]
      utime.sleep(0.1)

      # scale factor acc
      self.ACC_SCALE_FACTOR = acc.ACC_SCALE_FACTORS[accel_sensitive_range]
      utime.sleep(0.1)

      # set PMU mode for gyroscope to normal
      self.cmd(cmds.GYR_MODE_NORMAL)
      utime.sleep(0.1)

      # set PMU mode for accelerometer to normal
      self.cmd(cmds.ACC_MODE_NORMAL)
      utime.sleep(0.1)

      while True:
        # read PMU status for accelerometer
        pmu_acc = self.i2c.readfrom_mem(0x69, 0x03, 1)
        pmu_acc_int = int.from_bytes(pmu_acc, 'big')
        pmu_acc_status = (pmu_acc_int >> 4) & 0x03
        pmu_gyr_status = (pmu_acc_int >> 2) & 0x03
        print("PMU ACC Status: ", pmu_acc_status)
        print("PMU GYR Status: ", pmu_gyr_status)
        if pmu_acc_status == 0x01 and pmu_gyr_status == 0x01:
          break
    
    def cmd(self, cmd):
       self.i2c.writeto_mem(0x69, 0x7E, bytearray([cmd]))

    ## combine register into 16 bits
    @micropython.viper
    def combine_h_l(self, high: uint, low: uint) -> int:
      val =  int((high << 8) | low)
      # check if sign bit is set a two's complement must be applied
      if high & 0x80:
          val = val - 65536 # equivalent to temp_val = -((temp_val ^ 0xFFFF) + 1)
      return val
    
    def read_gyro_raw(self):
      gyr_x_lsb = self.i2c.readfrom_mem(0x69, 0x0C, 1)
      gyr_x_msb = self.i2c.readfrom_mem(0x69, 0x0D, 1)
      gx = self.combine_h_l(gyr_x_msb[0], gyr_x_lsb[0])

      gyr_y_lsb = self.i2c.readfrom_mem(0x69, 0x0E, 1)
      gyr_y_msb = self.i2c.readfrom_mem(0x69, 0x0F, 1)
      gy = self.combine_h_l(gyr_y_msb[0], gyr_y_lsb[0])

      gyr_z_lsb = self.i2c.readfrom_mem(0x69, 0x10, 1)
      gyr_z_msb = self.i2c.readfrom_mem(0x69, 0x11, 1)
      gz = self.combine_h_l(gyr_z_msb[0], gyr_z_lsb[0])

      gx = gx * self.GYR_SCALE_FACTOR
      gy = gy * self.GYR_SCALE_FACTOR
      gz = gz * self.GYR_SCALE_FACTOR

      return gx, gy, gz
    
    def read_accel_raw(self):
      acc_x_lsb = self.i2c.readfrom_mem(0x69, 0x12, 1)
      acc_x_msb = self.i2c.readfrom_mem(0x69, 0x13, 1)
      ax = self.combine_h_l(acc_x_msb[0], acc_x_lsb[0])

      acc_y_lsb = self.i2c.readfrom_mem(0x69, 0x14, 1)
      acc_y_msb = self.i2c.readfrom_mem(0x69, 0x15, 1)
      ay = self.combine_h_l(acc_y_msb[0], acc_y_lsb[0])

      acc_z_lsb = self.i2c.readfrom_mem(0x69, 0x16, 1)
      acc_z_msb = self.i2c.readfrom_mem(0x69, 0x17, 1)
      az = self.combine_h_l(acc_z_msb[0], acc_z_lsb[0])

      ax = ax * self.ACC_SCALE_FACTOR
      ay = ay * self.ACC_SCALE_FACTOR
      az = az * self.ACC_SCALE_FACTOR

      return ax, ay, az
    
    def read_temp_celsius(self):
      ## read temperature
      # A temperatura é expressa em unidades de 1/512 graus por LSB. O valor 0 corresponde a 23°C.
      # Leia o registro de temperatura
      temp_data = self.i2c.readfrom_mem(0x69, 0x20, 2)
      # Converta os dados do registro de temperatura em uma temperatura em graus Celsius
      temp = self.combine_h_l(temp_data[1], temp_data[0])
      temp = 23 + (temp / 512.0)

      return temp
    ## calibrate the accelerometer
    def calibrate_accel(self):
      # Rotate the sensor around all axes 90 degrees to calibrate the accelerometer
      # x, y, and should have +/- 1g of acceleration
      axTotal, ayTotal, azTotal = 0, 0, 0
      for y in range(1):
        print("Calibrating accelerometer... ", y)
        for i in range(1000):
          ax, ay, az = self.read_accel_raw()
          axTotal += ax
          ayTotal += ay
          azTotal += az

      axTotal = axTotal / 1000
      ayTotal = ayTotal / 1000
      azTotal = azTotal / 1000

      axAbs = abs(axTotal)
      ayAbs = abs(ayTotal)
      azAbs = abs(azTotal)

      print("azTotal: ", azTotal)

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

      # minus 1g
      offset = offset - 9.81

      return {
        useAccel: offset,
      }
      
    ## calibrate the gyroscope
    def calibrate_gyro(self):
      # Calibrate the gyroscope
      # The gyroscope is calibrated by reading the average value of the gyroscope data when the sensor is at rest
      # Wait for MPU to Settle
      gxTotal, gyTotal, gzTotal = 0, 0, 0
      for y in range(10):
        print("Calibrating gyroscope... ", y)
        for i in range(1000):
          gx, gy, gz = self.read_gyro_raw()
          gxTotal += gx
          gyTotal += gy
          gzTotal += gz

      return {
        'gx': gxTotal / 10000,
        'gy': gyTotal / 10000,
        'gz': gzTotal / 10000
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
    
    def manual_offset(self):
      print('to do')
      # ########## Some how works
      # ### 1. Enable manual offset for gyroscope before calibration!!!
      # ## Habilitar o offset manual para o giroscópio
      # # Se habilitar é necessário trocar os valores de offset
      # current_value = i2c.readfrom_mem(0x69, 0x77, 1)[0]
      # # Defina o bit 7 para 1, mantendo os outros bits como estão
      # new_value = current_value | 0b10000000
      # # Escreva o novo valor de volta no registro
      # i2c.writeto_mem(0x69, 0x77, bytearray([new_value]))
      # utime.sleep(0.1)

      # ### 2. Calibrate the gyroscope (results are in °/s), results are not as expected
      # # offsets = {'gy': 150.8756, 'gz': 57.118, 'gx': 37.0541}
      # offsets = {'gy': -10.8756, 'gz': -8.118, 'gx': 5.0541}

      # # Converta os valores de offset de °/s para a representação do LSB e arredonde para o número inteiro mais próximo
      # offsets_lsb = {axis: round(offset) for axis, offset in offsets.items()}
      # # offsets_lsb = {axis: round(offset / 16.4) for axis, offset in offsets.items()}

      # # Converta os números para uma representação de bytes, tratando-os como um número de complemento de dois
      # offsets_bytes = {axis: ustruct.pack('h', offset_lsb) for axis, offset_lsb in offsets_lsb.items()}

      # # Escreva os valores de offset nos registros de offset apropriados
      # i2c.writeto_mem(0x69, 0x74, bytearray([offsets_bytes['gx'][0]]))  # gx
      # i2c.writeto_mem(0x69, 0x75, bytearray([offsets_bytes['gy'][0]]))  # gy
      # i2c.writeto_mem(0x69, 0x76, bytearray([offsets_bytes['gz'][0]]))  # gz

      # # Para os 2 bits mais significativos, você precisa lê-los, limpar os bits apropriados, definir os bits e escrever de volta
      # reg_value = i2c.readfrom_mem(0x69, 0x77, 1)[0]

      # # Limpar os bits
      # reg_value &= ~(0b111111)

      # # Definir os bits para cada eixo
      # for axis, offset_bytes in offsets_bytes.items():
      #     two_most_significant_bits = (offset_bytes[1] & 0b11)
      #     if axis == 'gx':
      #         reg_value |= (two_most_significant_bits << 0)
      #     if axis == 'gy':
      #         reg_value |= (two_most_significant_bits << 2)
      #     if axis == 'gz':
      #         reg_value |= (two_most_significant_bits << 4)


      # # Escrever o valor de volta para o registro
      # i2c.writeto_mem(0x69, 0x77, bytearray([reg_value]))
      # utime.sleep(0.1)


# Usage
import ustruct
from machine import I2C, Pin
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)

bmi = BMI160(i2c)

# print(bmi.calibrate_accel())

# Offsets = {'gy': 0.7757404, 'gz': 0.5566668, 'gx': -0.2248721, 'az': 8.78165, 'ax': 8.874706, 'ay': 8.296988}
# Offsets = {'gy': 0.7757404, 'gz': 0.5566668, 'gx': -0.2248721, 'az': 0.02835, 'ax': -0.0935294, 'ay': -0.513012}
Offsets = {'gy': 0, 'gz': 0, 'gx': 0, 'az': 0, 'ax': 0, 'ay': 0}

while True:
  ax, ay, az, gx, gy, gz = bmi.get_acc_gyro(Offsets['ax'], Offsets['ay'], Offsets['az'], Offsets['gx'], Offsets['gy'], Offsets['gz'])
  # ax, ay, az = bmi.read_accel_raw()
  # temp = bmi.read_temp_celsius()
  # print("Gyro (°/s):", gx, gy, gz)
  # print("Accel (m/s²):", ax, ay, az)
  # print("Temp (°C):", temp)
  print(az)
  utime.sleep(0.05)