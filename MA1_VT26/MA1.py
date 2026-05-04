"""
Solutions to module 1
Student: Hugo Lovmar
Mail: hulo8756@student.uu.se
Reviewed by: Ivar Hammarberg
Reviewed date: 2026-04-08
"""

"""
Important notes: 
These examples are intended to practice RECURSIVE thinking. Thus, you may NOT 
use any loops nor built in functions like count, reverse, zip, math.pow etc. 

You may NOT use any global variables.

You can write code in the main function that demonstrates your solutions.
If you have testcode running at the top level (i.e. outside the main function)
you have to remove it before uploading your code into Studium!
Also remove all trace and debugging printouts!

You may not import any packages other than time and math and these may
only be used in the analysis of the fib function.

In the oral presentation you must be prepared to explain your code and make minor 
modifications.

We have used type hints in the code below (see 
https://docs.python.org/3/library/typing.html).
Type hints serve as documatation and and doesn't affect the execution at all. 
If your Python doesn't allow type hints you should update to a more modern version!

"""




import time
import math

def multiply(m: int, n: int) -> int:  
    """ Ex1: Computes m*n using additions"""
    if n == 0:
        return 0
    
    elif n > 0:
        return m + multiply(m, n-1)
    
    else: # for the situation when n is negative
        return -multiply(m, -n) # makes n positive and then makes the result of the new multiplication negative

# By first figuring out which of the two numbers are smaller, we can minimize the number of recursive calls since we will be adding the larger of the two numbers to tiself fewer times, instead of adding the smaller number to itself a bunch of times.

# if m < n:
#     return multiply(n, m)


def harmonic(n: int) -> float:              
    """Ex2: Computes and returns the harmonc sum 1 + 1/2 + 1/3 + ... + 1/n"""
    if n == 0:
        return 0
    
    else:
        return 1/n + harmonic(n-1)

def get_binary(x: int) -> str:              
    """ Ex3: Returns the binary representation of x """
    if x == 0:
        return '0'
    
    elif x == 1:
        return '1'
    
    elif x > 1:
        return get_binary(x//2) + str(x%2)
    
    else:
        return '-' + get_binary(-x)

def reverse_string(s: str) -> str:        
    """Ex4: Returns the s reversed """
    if s == '':
        return ''
    
    else:
        return s[-1] + reverse_string(s[:-1])


def largest(a: iter):                     
    """Ex5: Returns the largest element in a"""
    if len(a) == 1:
        return a[0]
    
    else:
        largest_element = largest(a[1:])

        if a[0] > largest_element:
            return a[0]
        
        else:
            return largest_element


def count(x, s: list) -> int:                
    """Ex6: Counts the number of occurences of x on all levels in s"""
    if s == []:
        return 0
    
    else:
        count_in_rest = count(x, s[1:])

        if s[0] == x:
            return 1 + count_in_rest
        
        elif type(s[0]) == list:
            return count(x, s[0]) + count_in_rest
        
        else:
            return count_in_rest


def bricklek(f: str, t: str, h: str, n: int) -> str:  
    """Ex7: Returns a string of instruction ow to move the tiles """
    if n == 0:
        return []
    
    else:
        return bricklek(f, h, t, n-1) + [f + '->' + t] + bricklek(h, t, f, n-1)


def fib(n: int) -> int:                      
    """ For Ex9: Returns the n:th Fibonacci number """
    # You should verify that the time for this function grows approximately as
    # Theta(1.618^n) and also estimate how long time the call fib(100) would take.
    # The time estimate for fib(100) should be in reasonable units (most certainly
    # years) and, since it is just an estimate, with no more than two digits precision.
    #
    # Put your code at the end of the main function below!
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)


def fib_mem(n) -> int:
    memory = {0:0, 1:1}

    def fib_mem2(n) -> int:
        if n not in memory:
            memory[n] = fib_mem2(n-1) + fib_mem2(n-2)
        return memory[n]
        
    return fib_mem2(n)


def main():
    print('\nCode that demonstates my implementations\n')

    print('\n\nCode for analysing fib and fib_mem\n')

    tstart = time.perf_counter()

    print(fib_mem(100))

    tstop = time.perf_counter()
    print(f"Measured time: {tstop-tstart} seconds")

    print('\nBye!')

if __name__ == "__main__":
    main()

####################################################

"""
  Answers to the none-coding tasks
  ================================
  
  
  Exercise 8: Time for the tile game with 50 tiles:
  
  The amount of moves needed to solve the tile game is n^2 - 1, where n is the number of tiles. If one were to have 50 tiles, the ampunt of moves needed to win the game would be 2^50 - 1, which is approx. 1.125 * 10^15 moves. If one move = one second, then it would take approx 35.7 million years to solve the game.
  

  
  Exercise 9: Time for Fibonacci:
    Test runs for fib:
    n: 30, Measured time: 0.19391520135104656 seconds
    n: 31, Measured time: 0.3388257008045912 seconds
    n: 32, Measured time: 0.5159882996231318 seconds
    n: 33, Measured time: 0.9813914000988007 seconds
    n: 34, Measured time: 1.5872988998889923 seconds
    n: 35, Measured time: 2.7549729999154806 seconds

    The ratio between time(n) and time(n-1) between these attempts is around the golden ratio, but for each attempt individually it's not exactly the same. The average of a large amount of attempts would probably get closer to the desired 1.618.

    To figure out the time for fib(50) we can get the time for fib(35) and then multiply it by 1.618^(50-35). Doing this gives us the answer of around 63 minutes for fib(50). Using the same technique for fib(100) (but this time using 1.618^(100-35)) gives us the answer of around 3.3 million years.
    

    
  Exercise 10: Time for fib_mem:
    The fibonacci number 100 is acccording to to fib_mem(100) equal to 354224848179261915075 and the time it took to calclate it was 0.00017750076949596405 seconds
  
  
  
  Exercise 11: Comparison sorting methods:
    If insertion sort and merge sort takes 1 second to sort 1000 random numbers the n the times for 10^6 and 10^9 numbers would be as follows (T = c * (n2/n1)^2) where c = 10^-6:
    
    Insertion sort:
    n: 10^6 time: 1000000 seconds (approx. 11.6 days)
    n: 10^9 time: 1000000000 seconds (approx. 31700 years)
    
    And for merge sort (T = c * (n log(n)) where c = 1/3 * 10^-4:

    Merge sort:
    n: 10^6 time: 2000 seconds (approx. 33.3 min)
    n: 10^9 time: 3000000 seconds (approx. 34.7 days)
  
  
  
  Exercise 12: Comparison Theta(n) and Theta(n log n)
    The test for algorithm B givves us that c = 0.1. Graphing the two functions y=x (symbolizing algo. A) and y=0.1*x*log(x) (symbolizing algo. B) we can see that the two functions intersect at around x = 10^10, which means at n > 10^10 it takes longer time for algo. B to run than for algo. A
  
"""
