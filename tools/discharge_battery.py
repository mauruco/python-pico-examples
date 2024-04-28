import machine, _thread

led = machine.Pin('LED', machine.Pin.OUT)
led.on()

def cpu_intensive_task():
    # Cálculo intensivo de CPU
    for _ in range(1000000):
        result = 3.1415926 * 2**0.5

led = machine.Pin(25, machine.Pin.OUT)

def Core0():
  while True:
    cpu_intensive_task()
        
def Core1():
  while True:
    led.toggle()

_thread.start_new_thread(Core1, ( ))
Core0()