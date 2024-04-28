from machine import Pin, I2C
import utime

# def combine_h_l(high, low):
#   val =  (high << 8) | low
#   # check if sign bit is set a two's complement must be applied
#   if high & 0x80:
#       val = val - 65536 # equivalent to temp_val = -((temp_val ^ 0xFFFF) + 1)
#   return val

# ### 
# i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)

# ## chip id
# chip_id = i2c.readfrom_mem(0x69, 0x00, 1)
# chip_id_int = int.from_bytes(chip_id, 'big') # Convert bytes to int


# ### read temperature
# # temp_lsb = i2c.readfrom_mem(0x69, 0x20, 1) # LSB
# # temp_msb = i2c.readfrom_mem(0x69, 0x21, 1) # MSB
# # temp = combine_h_l(temp_msb[0], temp_lsb[0])

# ### read sensor time, increments every 39 µs
# # sensor_time_lsb = i2c.readfrom_mem(0x69, 0x18, 1) # LSB
# # sensor_time_xsb = i2c.readfrom_mem(0x69, 0x19, 1) # XSB
# # sensor_time_msb = i2c.readfrom_mem(0x69, 0x1A, 1) # MSB

# # Combine LSB, XSB, and MSB
# # sensor_time = (sensor_time_msb[0] << 16) | (sensor_time_xsb[0] << 8) | sensor_time_lsb[0]

# ### accelerometer config, taxa de amostragem
# # 0x00: Desligado
# # 0x01: 0.78 Hz
# # 0x02: 1.56 Hz
# # 0x03: 3.12 Hz
# # 0x04: 6.25 Hz
# # 0x05: 12.5 Hz
# # 0x06: 25 Hz
# # 0x07: 50 Hz
# # 0x08: 100 Hz
# # 0x09: 200 Hz
# # 0x0A: 400 Hz
# # 0x0B: 800 Hz
# # 0x0C: 1600 Hz

# # Os bits 4 a 6 são usados para configurar a largura de banda do acelerômetro. Os valores possíveis são:
# # 0x00: Normal
# # 0x01: OSR2
# # 0x02: OSR4
# # 0x03: CIC (Continuous Integration and Combining)
# ##!! Configurations without a bandwidth number are illegal settings and will result in an error code in
# # the Register (0x02) ERR_REG.

# ### change acc range
# # 0x03 = +/- 2g
# # 0x05 = +/- 4g
# # 0x08 = +/- 8g
# # 0x0C = +/- 16g

# # Set accelerometer range to 2g
# # i2c.writeto_mem(0x69, 0x41, bytearray([0x03]))

# # Set accelerometer range to 4g
# # i2c.writeto_mem(0x69, 0x41, bytearray([0x05]))

# # Set accelerometer range to 8g
# # i2c.writeto_mem(0x69, 0x41, bytearray([0x08]))

# # # Set accelerometer range to 16g
# # i2c.writeto_mem(0x69, 0x41, bytearray([0x0C]))

# ### convert accelerometer data to m/s^2
# # 32767 = max value of 16-bit signed integer
# # 4     = 4g range
# # 9.81  = acceleration due to gravity
# # (acc_x / 32767.0) * 4 * 9.81
# # simplifying:
# # scale_factor = (4 / 32767.0) * 9.81
# # acc_x_m_s2 = acc_x * scale_factor


# ### gyro Config, taxa de amostragem
# # bits 0-3: gyro bandwidth
# # 0x06: 25 Hz
# # 0x07: 50 Hz
# # 0x08: 100 Hz
# # 0x09: 200 Hz
# # 0x0A: 400 Hz
# # 0x0B: 800 Hz
# # 0x0C: 1600 Hz
# # 0x0D: 3200 Hz

# # bits 4-5: gyr_bwp (gyro bandwidth parameter)
# # the gyroscope bandwidth coefficient defines the 3 dB cutoff frequency of the low pass
# # filter for the sensor data.
# #!! Configurations without a bandwidth number are illegal settings and will result in an error code in
# # the Register (0x02) ERR_REG.

# ## Set gyro bandwidth to 100 Hz
# # i2c.writeto_mem(0x69, 0x42, bytearray([0x08]))

# ### change gyro range
# # 0x00 +/- 2000°/s 16.4 LSB/°/s   61.0 m°/s / LSB
# # 0x01 +/- 1000°/s 32.8 LSB/°/s   30.5 m°/s / LSB
# # 0x02 +/- 500°/s  65.6 LSB/°/s   15.3 m°/s / LSB
# # 0x03 +/- 250°/s  131.2 LSB/°/s  7.6 m°/s  / LSB
# # 0x04 +/- 125°/s  262.4 LSB/°/s  3.8m°/s   / LSB
# # Set gyro range to 2000 dps
# # i2c.writeto_mem(0x69, 0x43, bytearray([0x00]))

# # # Set gyro range to 1000 dps
# # i2c.writeto_mem(0x69, 0x43, bytearray([0x01]))

# # # Set gyro range to 500 dps
# # i2c.writeto_mem(0x69, 0x43, bytearray([0x02]))

# # # Set gyro range to 250 dps
# # i2c.writeto_mem(0x69, 0x43, bytearray([0x03]))

# # # Set gyro range to 125 dps
# # i2c.writeto_mem(0x69, 0x43, bytearray([0x04]))

# ### convert gyro data to graus/s
# # 32767 = max value of 16-bit signed integer
# # 2000  = 2000 dps range
# # (gyr_x / 32767.0) * 2000
# # simplifying:
# # scale_factor = (2000 / 32767.0)
# # gyr_x_deg_s = gyr_x * scale_factor


# ###########
# # Soft reset, bring device to default state
# i2c.writeto_mem(0x69, 0x7E, bytearray([0xB6]))
# utime.sleep(0.1)

# # force the device into I2C comms mode
# i2c.readfrom_mem(0x69, 0x7F, 1)

# # set acc to 1600 Hz
# i2c.writeto_mem(0x69, 0x40, bytearray([0x0C]))
# utime.sleep(0.1)

# # set gyr to 1600 Hz
# i2c.writeto_mem(0x69, 0x42, bytearray([0x0C]))
# utime.sleep(0.1)

# # set accelerometer range to 8g
# i2c.writeto_mem(0x69, 0x41, bytearray([0x08]))
# utime.sleep(0.1)

# # set gyro range to 2000 dps
# i2c.writeto_mem(0x69, 0x43, bytearray([0x00]))
# utime.sleep(0.1)

# # set PMU mode for accelerometer to normal
# i2c.writeto_mem(0x69, 0x7E, bytearray([0x11]))
# utime.sleep(0.1)

# # set PMU mode for gyroscope to normal
# i2c.writeto_mem(0x69, 0x7E, bytearray([0x15]))
# utime.sleep(0.1)

# ## read
# # pmu acc
# pmu_acc = i2c.readfrom_mem(0x69, 0x03, 1)
# pmu_acc_int = int.from_bytes(pmu_acc, 'big') # Convert bytes to int
# pmu_acc_status = (pmu_acc_int >> 4) & 0x03
# print("PMU ACC Status: ", pmu_acc_status)

# # pmu gyr
# pmu_gyr = i2c.readfrom_mem(0x69, 0x03, 1)
# pmu_gyr_int = int.from_bytes(pmu_gyr, 'big') # Convert bytes to int
# pmu_gyr_status = (pmu_gyr_int >> 2) & 0x03
# print("PMU GYR Status: ", pmu_gyr_status)


# # Leia o valor do registro ACC_CONF
# acc_conf = i2c.readfrom_mem(0x69, 0x40, 1)[0]
# # Extraia os bits 0 a 3
# sample_rate_code = acc_conf & 0x0F
# # Converta o código da taxa de amostragem para a taxa de amostragem correspondente em Hz
# # Taxas de amostragem do acelerômetro
# sample_rate_acc = {
#     0x01: 0.78125,  # 0.78125 Hz
#     0x02: 1.5625,   # 1.5625 Hz
#     0x03: 3.125,    # 3.125 Hz
#     0x04: 6.25,     # 6.25 Hz
#     0x05: 12.5,     # 12.5 Hz
#     0x06: 25,       # 25 Hz
#     0x07: 50,       # 50 Hz
#     0x08: 100,      # 100 Hz
#     0x09: 200,      # 200 Hz
#     0x0A: 400,      # 400 Hz
#     0x0B: 800,      # 800 Hz
#     0x0C: 1600,     # 1600 Hz
# }
# sample_rate = sample_rate_acc[sample_rate_code]
# print("A taxa de amostragem do acelerômetro é", sample_rate, "Hz")

# # Leia o valor do registro GYR_CONF
# gyr_conf = i2c.readfrom_mem(0x69, 0x42, 1)[0]
# # Extraia os bits 0 a 3
# sample_rate_code = gyr_conf & 0x0F
# # Converta o código da taxa de amostragem para a taxa de amostragem correspondente em Hz
# sample_rate_gyr = {
#     0x06: 25,       # 25 Hz
#     0x07: 50,       # 50 Hz
#     0x08: 100,      # 100 Hz
#     0x09: 200,      # 200 Hz
#     0x0A: 400,      # 400 Hz
#     0x0B: 800,      # 800 Hz
#     0x0C: 1600,     # 1600 Hz
#     0x0D: 3200,     # 3200 Hz
# }
# sample_rate = sample_rate_gyr[sample_rate_code]
# print("A taxa de amostragem do giroscópio é", sample_rate, "Hz")

# ## read temperature
# # A temperatura é expressa em unidades de 1/512 graus por LSB. O valor 0 corresponde a 23°C.
# # Leia o registro de temperatura
# temp_data = i2c.readfrom_mem(0x69, 0x20, 2)
# # Converta os dados do registro de temperatura em uma temperatura em graus Celsius
# temp = ((temp_data[1] << 8) | temp_data[0])
# if temp > 32767:  # se o valor for negativo no complemento de dois
#     temp -= 65536  # subtraia 2^16 para obter o valor correto
# temp = 23 + (temp / 512.0)

# print(f"Temperature: {temp} °C")

# while True:
#   accel_x_lsb = i2c.readfrom_mem(0x69, 0x12, 1) # LSB
#   accel_x_msb = i2c.readfrom_mem(0x69, 0x13, 1) # MSB
#   accel_x = combine_h_l(accel_x_msb[0], accel_x_lsb[0])
#   ax = (accel_x / 32767.0) * 8 * 9.81
#   print("Accel X: ", ax)
#   utime.sleep(1)