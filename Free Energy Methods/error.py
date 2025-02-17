import sys
import math
import numpy as np
import random

if len(sys.argv) != 4:
    print("Finite Difference Thermodynamic Integration (Mezei 1987)")
    print("Trapezoidal integration of compute_fep results at equally-spaced points")
    print("usage: error.py temperature < out.fep")
    sys.exit()

rt = 0.008314 / 4.184 * float(sys.argv[1]) # in kcal/mol


boltzman_distribution = []
for line in sys.stdin:
    while line.startswith("#"):
        line = sys.stdin.readline()
    tok = line.split()
    boltzman_distribution.append((float(tok[2])))



def FDTI(boltzman):
    RT = (0.008314 / 4.184) * float(sys.argv[1]) 
    hderiv = float(sys.argv[2])
    v = 1.0
    lo = -RT * math.log(boltzman[0] / v)
    i = 1
    sum = 0.0
    for j in range(1,int(len(boltzman))):
        hi = - RT * math.log(boltzman[j] / v)
        sum += (hi + lo) / (2 * hderiv)
        lo = hi
        i += 1

    free_energy = (sum/(i - 1))
    f1 = -RT * np.log(boltzman)
    std_error = np.std(f1, ddof=1) / np.sqrt(len(f1))
    
    
    return free_energy,std_error


def resample(data, seed):
    '''
    Creates a resample of the provided data that is the same length as the provided data
    '''
    random.seed(seed)
    res = random.choices(data, k=len(data))
    return res

boot_resamples = [resample(boltzman_distribution, val) for val in range(int(sys.argv[3]))]
F = [FDTI(res)[0] for res in boot_resamples]
std_e = [FDTI(res)[1] for res in boot_resamples]

print(np.std(F,ddof=1)/np.sqrt(len(F)))



