# sensivity values for the gyroscope, °/s
GYR_2000 = const(0x00)
GYR_1000 = const(0x01)
GYR_500 = const(0x02)
GYR_250 = const(0x03)
GYR_125 = const(0x04)

# rate values for the gyroscope, Hz
GYR_RATE_25 = const(0x06)
GYR_RATE_50 = const(0x07)
GYR_RATE_100 = const(0x08)
GYR_RATE_200 = const(0x09)
GYR_RATE_400 = const(0x0A)
GYR_RATE_800 = const(0x0B)
GYR_RATE_1600 = const(0x0C)
GYR_RATE_3200 = const(0x0D)

# scale factor for the gyroscope, °/s
### convert gyro data to °/s
# 32767 = max value of 16-bit signed integer
# 2000  = 2000 dps range
# (gyr_x / 32767.0) * 2000
# simplifying:
# scale_factor = (2000 / 32767.0)
# gyr_x_deg_s = gyr_x * scale_factor
GYR_SCALE_FACTORS = {
  GYR_2000: 2000 / 32767.0,
  GYR_1000: 1000 / 32767.0,
  GYR_500: 500 / 32767.0,
  GYR_250: 250 / 32767.0,
  GYR_125: 125 / 32767.0
}