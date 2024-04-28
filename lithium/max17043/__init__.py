import utime as time

## MAX17043 - Monitor de Bateria de Íon de Lítio
# Estado de Carga (SOC): O SOC é uma estimativa da quantidade de energia restante na bateria. O MAX17043 fornece o SOC como um valor de 16 bits, onde os 8 bits mais significativos representam a porcentagem da bateria e os 8 bits menos significativos representam a fração de 1/256%.
# Tensão da Célula (VCELL): O MAX17043 pode medir a tensão da célula da bateria. A tensão é fornecida como um valor de 12 bits com uma resolução de 1.25mV.
# Versão do IC (VERSION): O MAX17043 tem um registro de versão que pode ser lido para determinar a versão do IC.
# Configuração (CONFIG): O MAX17043 tem um registro de configuração que pode ser usado para configurar várias configurações do IC, como o valor do resistor de detecção e o limiar de alerta de bateria baixa.
# Alerta de Bateria Baixa (ALRT): O MAX17043 pode gerar um sinal de alerta quando o SOC cai abaixo de um limiar especificado. O limiar de alerta pode ser configurado no registro de configuração.
# Comando de Controle (COMMAND): O MAX17043 tem um registro de comando que pode ser usado para enviar comandos de controle para o IC, como um comando de "reset".

"""
  # How to use the MAX17043 class:
  import machine
  import MAX17043

  I2C_SDA_PIN = 14
  I2C_SCL_PIN = 15
  I2C_ID=1 # id=1 See Pinout diagram (id=1 == sda2 and scl3)

  max17043 = MAX17043(machine.I2C(I2C_ID, sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN)))

  # print version
  print('IC Version:', max17043.read_ic_version())

  # print battery percentage
  print('Battery Percentage:', max17043.read_battery_percentage())

  # print battery voltage
  print('Battery Voltage:', max17043.read_battery_voltage())
"""


# Endereço I2C do MAX17043
MAX17043_ADDRESS = const(0x36)

# Registros do MAX17043
REG_VCELL = const(0x02)
REG_SOC = const(0x04)
REG_MODE = const(0x06)
REG_VERSION = const(0x08)
REG_CONFIG = const(0x0C)
REG_COMMAND = const(0xFE)

class MAX17043:
  def __init__(self, i2c, address=MAX17043_ADDRESS):
    self.i2c = i2c
    self.address = address
    # Escreva 0x5400 no registro COMMAND para resetar o MAX17043
    i2c.writeto_mem(self.address, REG_COMMAND, bytearray([0x54, 0x00]))
    # Aguarde o MAX17043 inicializar
    time.sleep(1)
    # Escreva 0x4000 no registro CONFIG para definir o resistor de detecção para 32kOhm (padrão)
    i2c.writeto_mem(self.address, REG_CONFIG, bytearray([0x40, 0x00]))

  # Used for recalibration??
  def quick_start(self):
    # Escreva 0x4000 no registro MODE para iniciar uma conversão de capacidade de carga rápida
    self.i2c.writeto_mem(self.address, REG_MODE, bytearray([0x40, 0x00]))

  def read_ic_version(self):
    # Leia 2 bytes do registro VERSION
    data = self.i2c.readfrom_mem(self.address, REG_VERSION, 2)
    
    # Os dados são em formato big endian, então converta para um número
    version = (data[0] << 8) | data[1]
    
    return version

  def read_battery_percentage(self):
    # Leia 2 bytes do registro SOC
    data = self.i2c.readfrom_mem(self.address, REG_SOC, 2)
    
    # Os dados são em formato big endian, então converta para um número
    # O estado de carga é representado pelo primeiro byte inteiro e os 8 bits menos significativos representam a fração de 1/256%
    percentage = data[0] + data[1] / 256.0
    
    return '{:.2f}%'.format(percentage)

  def read_battery_voltage(self):
    # Leia 2 bytes do registro VCELL
    data = self.i2c.readfrom_mem(self.address, REG_VCELL, 2)
    
    # Os dados são em formato big endian, então converta para um número
    # A tensão é representada pelos 12 bits mais significativos com resolução de 1.25mV
    voltage = ((data[0] << 4) | (data[1] >> 4)) * 1.25 / 1000.0
    
    return '{:.2f}V'.format(voltage)
