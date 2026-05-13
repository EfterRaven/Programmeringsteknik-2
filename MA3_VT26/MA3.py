""" MA3.py

Student: Hugo Lovmar
Mail: hlovmar@gmail.com
Reviewed by: Isac Persson
Date reviewed: 2025-05-13

"""
import random
import matplotlib.pyplot as plt
import math as m
import concurrent.futures as future
from statistics import mean 
from time import perf_counter as pc

def approximate_pi(n): # Ex1
    nc = 0
    x_in, y_in = [], []
    x_out, y_out = [], []

    # generate points and see if they are inside or outside the circle
    for _ in range(n):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        
        if x**2 + y**2 <= 1:
            nc += 1
            x_in.append(x)
            y_in.append(y)
        else:
            x_out.append(x)
            y_out.append(y)

    pi_approx = 4 * nc / n
    print(f"Approximation of pi: {pi_approx} if n={n}")

    # Produce a plot with red inside dots and blue outside dots
    plt.figure(figsize=(5, 5))
    plt.scatter(x_in, y_in, color='red', s=1, label='Inside')
    plt.scatter(x_out, y_out, color='blue', s=1, label='Outside')
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.title(f"Pi Approximation = {pi_approx}  (n={n})")
    plt.savefig(f"pi_approximation_{n}.png")
    plt.close()
    
    return pi_approx

def sphere_volume(n, d): #Ex2, approximation
    #n is the number of points
    # d is the number of dimensions of the sphere 
    points = [[random.uniform(-1, 1) for _ in range(d)] for _ in range(n)]
    
    inside_points = list(filter(lambda p: sum(map(lambda x: x**2, p)) <= 1, points))
    
    # (points inside/total points) * volume of the "cube"
    return (len(inside_points) / n) * (2**d)

def hypersphere_exact(d): #Ex2, real value
    #n is the number of points
    # d is the number of dimensions of the sphere 
    return (m.pi**(d/2)) / m.gamma(d/2 + 1)

#Ex3: parallel code - parallelize for loop
def sphere_volume_parallel1(n, d, np = 10):
    with future.ProcessPoolExecutor(max_workers = np) as executor:
        results = list(executor.map(sphere_volume, [n]*np, [d]*np))
    
    # Return the average value
    return sum(results) / len(results)

# This Exercise 3 failed in the test on my own laptop, but passed the test on the Linux Machine.
# The parallel version (2.4s) was faster by about a second compared to the sequantial version(3.2s), which is an improvement. On the linux machine, the sequential version took a whole 8.7s seconds, while the parallel version took 1.8 seconds, a significant improvement.

#Ex4: parallel code - parallelize actual computations by splitting data
def sphere_volume_parallel2(n, d, np = 10):
    n_per_process = n // np

    with future.ProcessPoolExecutor(max_workers = 10) as executor:
        results = list(executor.map(sphere_volume, [n_per_process]*np, [d]*np))
    
    # Return the average value
    return sum(results) / len(results)
    
#The paralell version (2.4s) wast faster by about a second compared to the sequantial version(3.3s), which is an improvement. On the linux machine, the sequantial version took 9.4s, compared to the parallel time of 1.6s, which is a lrge improvement.

def main():
    #Ex1
    dots = [1000, 10000, 100000]
    for n in dots:
        approximate_pi(n)

    #Ex2
    n = 100000
    d = 2
    print(f"Approx. volume of {d} dimentional sphere = {sphere_volume(n,d)}")
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    n = 100000
    d = 11
    print(f"Approx. volume of {d} dimentional sphere = {sphere_volume(n,d)}")
    print(f"Actual volume of {d} dimentional sphere = {hypersphere_exact(n,d)}")

    #Ex3
    n = 100000
    d = 11
    start = pc()
    for y in range (10):
        sphere_volume(n,d)
    stop = pc()
    print(f"Ex3: Sequential time of {d} and {n}: {stop-start}")
    start = pc()

    start = pc()
    sphere_volume_parallel1(n,d,np=10)
    stop = pc()
    print(f"Ex3: Parallel time of {d} and {n}: {stop-start}")

    #Ex4
    n = 1000000
    d = 11
    start = pc()
    sphere_volume(n,d)
    stop = pc()
    print(f"Ex4: Sequential time of {d} and {n}: {stop-start}")
    
    start = pc()
    sphere_volume_parallel2(n,d,np=10)
    stop = pc()
    print(f"Ex4: Parallel time of {d} and {n}: {stop-start}")

    
    

if __name__ == '__main__':
	main()
