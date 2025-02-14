import sys
import math
import numpy as np

if len(sys.argv) != 2:
    print("Finite Difference Thermodynamic Integration (Mezei 1987)")
    print("Trapezoidal integration of compute_fep results at equally-spaced points")
    print("usage: error.py temperature < out.fep")
    sys.exit()

rt = 0.008314 / 4.184 * float(sys.argv[1]) # in kcal/mol


f = []
for line in sys.stdin:
    while line.startswith("#"):
        line = sys.stdin.readline()
    tok = line.split()
    f.append(-rt*np.log(float(tok[2])))

F = [(i-np.average(f))**2 for i in f]

print(f"{(np.sqrt(sum(F)/len(F)))/np.sqrt(len(F)-1):<10.5f}")



