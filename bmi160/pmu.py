# pmu is readyonly
# acc_pmu_status = bits 5:4
# gyr_pmu_status = bits 3:2
# mag_pmu_status = bits 1:0

# acc_pmu_status Accel Mode
# 0b00 Suspend
# 0b01 Normal
# 0b10 Low Power

# gyr_pmu_status Gyro Mode
# 0b00 Suspend
# 0b01 Normal
# 0b10 Reserved
# 0b11 Fast Start-Up

# mag_pmu_status Magnet Mode
# 0b00 Suspend
# 0b01 Normal
# 0b10 Low Power

## Extract status
# pmu_status = i2c.readfrom_mem(0x69, 0x03, 1)
# pmu_status_int = int.from_bytes(pmu_status, 'big') # Convert bytes to int

# # Extract acc_pmu_status
# acc_pmu_status = (pmu_status_int >> 4) & 0x03

# print(acc_pmu_status)

# # Extract gyr_pmu_status
# gyr_pmu_status = (pmu_status_int >> 2) & 0x03
