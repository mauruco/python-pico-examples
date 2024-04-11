from machine import I2C, PIN
import cmds

class BMI160:
    def __init__(self, i2c, gyro_sensitive_range = 2, accel_sensitive_range = 2):
      self.i2c = i2c

      # check chip id
      chip_id = i2c.readfrom_mem(0x69, 0x00, 1)
      chip_id_int = int.from_bytes(chip_id, 'big') # Convert bytes to int
      if chip_id_int != 0xD1:
        raise ValueError("Invalid chip id: %x" % chip_id_int)
      
      print("BMI160 initialized")

      # reset to default state
      self.cmd(cmds.SOFT_RESET)

      # force  I2C commons mode
      i2c.readfrom_mem(0x69, 0x7F, 1)

      
    
    def cmd(self, cmd):
       self.i2c.writeto_mem(0x69, 0x7E, bytearray([cmd]))
