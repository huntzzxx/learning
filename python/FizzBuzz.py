#! python3
# FizzBuzz.py - FizzBuzz program that prints numbers from 1 to n, but for multiples of 3, prints "Fizz" instead of the number, and for multiples of 5, prints "Buzz" instead of the number. For numbers which are multiples of both three and five, prints "FizzBuzz".

def fizzBuzz(n):
    for i in range(1, n+1):
        if i % 3 == 0 and i % 5 == 0:
            print("FizzBuzz")
            i=i+1
        elif i % 3 == 0:
            print("Fizz")
            i=i+1
        elif i % 5 == 0:
            print("Buzz")
            i=i+1
        else:
            print(i)
            i=i+1