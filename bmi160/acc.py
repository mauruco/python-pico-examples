# sensitivity values for the accelerometer
ACC_2G = const(0x03)
ACC_4G = const(0x05)
ACC_8G = const(0x08)
ACC_16G = const(0x0C)

# rate values for the accelerometer, Hz
ACC_RATE_0_78 = const(0x01)
ACC_RATE_1_56 = const(0x02)
ACC_RATE_3_12 = const(0x03)
ACC_RATE_6_25 = const(0x04)
ACC_RATE_12_5 = const(0x05)
ACC_RATE_25 = const(0x06)
ACC_RATE_50 = const(0x07)
ACC_RATE_100 = const(0x08)
ACC_RATE_200 = const(0x09)
ACC_RATE_400 = const(0x0A)
ACC_RATE_800 = const(0x0B)
ACC_RATE_1600 = const(0x0C)

# scale factor for the accelerometer, g
### convert accelerometer data to m/s^2
# 32767 = max value of 16-bit signed integer
# 4     = 4g range
# 9.81  = acceleration due to gravity
# (acc_x / 32767.0) * 4 * 9.81
# simplifying:
# scale_factor = (4 / 32767.0) * 9.81
# acc_x_m_s2 = acc_x * scale_factor
ACC_SCALE_FACTORS = {
  ACC_2G: 2 / 32767.0 * 9.81,
  ACC_4G: 4 / 32767.0 * 9.81,
  ACC_8G: 8 / 32767.0 * 9.81,
  ACC_16G: 16 / 32767.0 * 9.81
}