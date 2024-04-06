import utime
from compiled.benchmark_factorial_compiled import factorial_compiled
from compiled.benchmark_factorial_compiled_native import factorial_compiled as factorial_compiled_native
from compiled.benchmark_factorial_compiled_viper_uint import factorial_viper_uint as factorial_comp_viper_uint

## results on pico 2040
# When it comes to raw performance, "NOT" compiling with viper and native is the way to go.
# Function timed_factorial_no_optimiz Time ~=  0.739ms
# Function timed_factorial___compiled Time ~=  0.734ms
# Function timed_factorial_compil_nat Time ~=  0.525ms
# Function timed_factorial_native_emi Time ~=  0.513ms
# Function timed_factorial_viper__int Time ~=  0.320ms
# Function timed_factorial_viper_uint Time ~=  0.318ms
# Function timed_factorialcviper_uint Time ~=  0.331ms

def timed_function(f, *args, **kwargs):
  myname = str(f).split(' ')[1]
  def new_func(*args, **kwargs):
    t = utime.ticks_us()
    result = f(*args, **kwargs)
    delta = utime.ticks_diff(utime.ticks_us(), t)
    print('Function {} Time = {:6.3f}ms'.format(myname, delta/1000))
    return result
  return new_func

# no optimization
def factorial__no_optimi(n):
  if n == 0:
      return 1
  else:
    return n * factorial__no_optimi(n-1)
  
@timed_function
def timed_factorial_no_optimiz():
    return factorial__no_optimi(27)

# compiled
@timed_function
def timed_factorial___compiled():
    return factorial_compiled(27)

# compiled native emitter
@timed_function
def timed_factorial_compil_nat():
    return factorial_compiled_native(27)

# native emitter
@micropython.native
def factorial_native_emi(n):
  if n == 0:
      return 1
  else:
    return n * factorial_native_emi(n-1)
    
@timed_function
def timed_factorial_native_emi():
    return factorial_native_emi(27)


# viper int
@micropython.viper
def factorial_viper_int(n: uint) -> uint: 
  if n == uint(0):
    return uint(1)
  else:
    nn = factorial_viper_int(n-1)
    return n * uint(nn)
    
@timed_function
def timed_factorial_viper__int():
    return factorial_viper_int(27)


# viper uint
@micropython.viper
def factorial_viper_uint(n: uint) -> uint: 
  if n == uint(0):
    return uint(1)
  else:
    nn = factorial_viper_uint(n-1)
    return n * uint(nn)
    
@timed_function
def timed_factorial_viper_uint():
    return factorial_viper_uint(27)

# viper compiled uint
@timed_function
def timed_factorialcviper_uint():
    return factorial_comp_viper_uint(27)


while True:
  print('---------------------------------------------------')
  timed_factorial_no_optimiz()
  timed_factorial___compiled()
  timed_factorial_compil_nat()
  timed_factorial_native_emi()
  timed_factorial_viper__int()
  timed_factorial_viper_uint()
  timed_factorialcviper_uint()
  utime.sleep(1)