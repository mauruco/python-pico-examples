## compiled factorial function
# ./mpy-cross -march=armv6m -X emit=viper benchmark_factorial_compiled.py

def factorial_viper_uint(n: uint) -> uint: 
  if n == uint(0):
    return uint(1)
  else:
    nn = factorial_viper_uint(n-1)
    return n * uint(nn)