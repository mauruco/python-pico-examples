## compiled factorial function
# ./mpy-cross benchmark_factorial_compiled.py
# ./mpy-cross -march=armv6m -X emit=native benchmark_factorial_compiled.py

def factorial_compiled(n):
  if n == 0:
      return 1
  else:
    return n * factorial_compiled(n-1)