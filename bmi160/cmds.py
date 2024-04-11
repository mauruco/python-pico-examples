### CMDS
# command definitions
## Starts Fast Offset Calibration for the accel and gyro as configured in Register (0x69), FOC_CONF and stores the result into the Register (0x71-0x77) OFFSET register.
START_FOC       = const(0x03) 
## Sets the PMU mode for the accelerometer. The encoding for ‘nn’ is identical to acc_pmu_status in Register (0x03) PMU_STATUS.
ACC_MODE_NORMAL = const(0x11)
## Sets the PMU mode for the gyroscope. The encoding for ‘nn’ is identical to gyr_pmu_status in Register (0x03) PMU_STATUS
GYR_MODE_NORMAL = const(0x15)
## clears all data in the FIFO, does not change the Register (0x46-0x47) FIFO_CONFIG and Register (0x45) FIFO_DOWNS registers.
FIFO_FLUSH      = const(0xB0)
## resets the interrupt engine, the Register (0x1C-0x1F) INT_STATUS and the interrupt pin.
INT_RESET       = const(0xB1)
## triggers a reset of the step counter. This register is functional in all operation modes. 
STEP_CNT_CLR    = const(0xB2)
## triggers a reset including a reboot.
SOFT_RESET      = const(0xB6)