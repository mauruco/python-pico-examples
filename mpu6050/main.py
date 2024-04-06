from machine import Pin, I2C
from mpu6050 import MPU6050

### IMPORTANT Do not forget to calibrate the MPU6050

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

### Calibrate accelerometer
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
mpu6050 = MPU6050(0x68, i2c)

# do not move the sensor during calibration
print('Calibrating accelerometer...')
print(mpu6050.calibrate_gyro())
# calibrate the accelerometer Z axis
# do not move the sensor during calibration
print(mpu6050.calibrate_accel())
# now rotate the x axis 90 degrees
print(mpu6050.calibrate_accel())
# now rotate the y axis 90 degrees
print(mpu6050.calibrate_accel())

### How to use
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
mpu6050 = MPU6050(0x68, i2c)
# AX, AY, AZ
offsetsA = [0.0585127, -0.0130398, 0.02573442] # results from calibrate_accel()
# GX, GY, GZ
offsetsG =  [-4.043702 , -0.7225068 , -0.6325746] # results from calibrate_gyro()
# AX, AY, AZ, GX, GY, GZ
offsets = offsetsA + offsetsG
while True:
  ax, ay, az, gx, gy, gz = mpu6050.get_acc_gyro(offsets[0], offsets[1], offsets[2], offsets[3], offsets[4], offsets[5])
  print('ax %.5f ay %.5f az %.5f pitch %.5f roll %.5f yaw %.5f' % (ax, ay, az, gx, gy, gz))

  # invert some axis to match Euler angles convention
  # when solder points of the MPU6050 are facing left, use the following
  # ax = -ax, ay = -az, az = ay, pitch = -gx, roll = gy, gz = -gz
  # print('ax %.5f ay %.5f az %.5f pitch %.5f roll %.5f yaw %.5f' % (-ax, -az, ay, gx, gy, -gz))

  # when solder points of the MPU6050 are facing up, use the following
  # print('az %.5f ay %.5f ax %.5f roll %.5f pitch %.5f yaw %.5f' % (-ax, -az, -ay, -gx, gy, -gz))


  # when solder points of the MPU6050 are facing right, use the following
  # print('ax %.5f ay %.5f az %.5f pitch %.5f roll %.5f yaw %.5f' % (ax, -az, -ay, -gx, -gy, -gz))

  # sleep(0.01)

### Calculate angles using gyro and accelerometer
from machine import Pin, I2C
import utime
from math import atan, sqrt, pi, sin

i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
mpu6050 = MPU6050(0x68, i2c)

offsetsA = [0.0585127, -0.0130398, 0.02573442] # results from calibrate_accel()
offsetsG =  [-4.043702 , -0.7225068 , -0.6325746] # results from calibrate_gyro()
offsets = offsetsA + offsetsG

anglePitch = 0
angleRoll = 0
uStart=utime.ticks_ms()
while True:
  ## USING GYROSCOPE
  # digamos que ele está girando em torno do eixo x na velocidade de 1 grau por segundo
  # digamos que estamos apenas fazendo uma leitura por segundo
  # digamos que o fizemos isso por 60 segundos
  # então o valor de gx seria 60 graus
  # a ideia é essa
  # só que estamos trabalhando com milisegundos, e temos que monitorar o tempo que levou para fazer a leitura
  # como estamos trabalhando com milisegundos, temos que converter para segundos multiplicando por 0.001
  # notei que o resultado é mais exato se eu usar a média do tempo de processo do loop inteiro e multiplicar por 0.001
  # a parte de transferir a rotação para o roll pitch é um pouco mais complicada
  # a ideia é que a rotação do roll e pitch são influenciadas pela rotação do yaw
  uStart=utime.ticks_ms()
  ax, ay, az, gx, gy, gz = mpu6050.get_acc_gyro(offsets[0], offsets[1], offsets[2], offsets[3], offsets[4], offsets[5])
  print('gx %.5f gy %.5f gz %.5f' % (gx, gy, gz))
  uEnd=utime.ticks_ms()

  # uLoop=(uEnd-uStart) * 0.001 # convert to seconds
  uLoop = 0.0026096 # each much accurate when you take the average of the intire loop time and multiply by 0.001
  anglePitch += gx * uLoop
  angleRoll += gy * uLoop
  print('Pitch: ', anglePitch)

  ## USING ACCELEROMETER
  # obtendo o vetor de aceleração total
  # podemos usar isso para calcular o ângulo de inclinação
  # assim podemos aplicar Pitagores para obter os outros ângulos
  ax, ay, az, gx, gy, gz = mpu6050.get_acc_gyro(offsets[0], offsets[1], offsets[2], offsets[3], offsets[4], offsets[5])
  totalAccelVector = sqrt(ax * ax + ay * ay + az * az)
  anglePitch = atan(ay / sqrt(ax * ax + az * az)) * 180 / pi
  angleRoll = atan(-ax / sqrt(ay * ay + az * az)) * 180 / pi

  # drift compensation
  # get a large portion of angle and a small portion of the acceleration for drift compensation
  angleRoll = angleRoll * 0.9996 + (ay * 0.0004)
  anglePitch = anglePitch * 0.9996 + (ax * 0.0004)
  print('Roll: ', angleRoll)
  sleep(0.1)