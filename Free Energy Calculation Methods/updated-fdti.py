#!/usr/bin/env python
# fdti.py - integrate compute fep results using the trapezoidal rule with error estimation

import sys
import math
import numpy as np

if len(sys.argv) < 3:
    print("Finite Difference Thermodynamic Integration (Mezei 1987)")
    print("Trapezoidal integration of compute_fep results at equally-spaced points")
    print("usage: fdti.py temperature hderiv < out.fep")
    sys.exit()

# Parameters
rt = 0.008314 / 4.184 * float(sys.argv[1])  # in kcal/mol
hderiv = float(sys.argv[2])

# Read input and skip comments
lines = sys.stdin.readlines()
data = [line for line in lines if not line.startswith("#")]

# Parse and calculate FDTI values
fdtis = []
lo = None
for i, line in enumerate(data):
    tok = line.split()
    if len(tok) != 3 and len(tok) != 4:
        continue

    v = 1.0
    if len(tok) == 4:
        v = float(tok[3])
    if i == 0:
        lo = -rt * math.log(float(tok[2]) / v)
        continue

    hi = -rt * math.log(float(tok[2]) / v)
    fdtis.append((hi + lo) / (2 * hderiv))
    lo = hi

def block_averaging(data, block_size):
    num_blocks = len(data) // block_size
    block_means = []

    for i in range(num_blocks):
        block = data[i * block_size : (i + 1) * block_size]
        block_means.append(np.mean(block))

    overall_mean = np.mean(block_means)
    error = np.std(block_means) / np.sqrt(num_blocks)  # Standard error of the mean
    return overall_mean, error


block_size = max(1, len(fdtis) // 7)  
mean_fdti, error_fdti = block_averaging(fdtis, block_size)

# Output results
print(f"FDTI Mean = {mean_fdti}")
print(f"Error (Standard Error = ) {error_fdti}")

