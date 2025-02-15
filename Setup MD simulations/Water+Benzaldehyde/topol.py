import sys
import math
import pandas as pd
import numpy as np

numadso = 14

numWater = 2133
numbonds_ad = 14
numbonds = numWater*2 + numbonds_ad

numangles_ad = 21
numangles = numWater + numangles_ad

Mw_Hw = 1.007940
Mw_Ow = 15.999400
Mw_Rh = 102.90500
Mw_C = 12.011


numdihedrals = 28
numimpropers = 7
numatomType = 5
numbondType = 15
numangleType = 22
numdihedralsType = 28
numimpropersType = 7

atoms, index, x, y, z = [], [], [], [], []
with open('new-conf.gro') as f:
    for line in f:
        p = line.split()
        if len(p) == 8:
            atoms.append(p[0])
            index.append(p[1])
            x.append(float(p[2])*10)
            y.append(float(p[3])*10)
            z.append(float(p[4])*10)
        elif len(p) == 3:
            lx = float(p[0])
            ly = float(p[1])
            lz = float(p[2])
            



names = [str('#'+i) for i in atoms]

molecule_id = []
f = 0
for i in range(0,3*numWater,3):
    f+=1
    for j in range(3):
        molecule_id.append(f)

for i in range(numadso):
    molecule_id.append(f+1)



mass_type = []
for i in range(len(atoms)):
    if atoms[i] == 'OW':
        mass_type.append(1)
    elif atoms[i] == 'HW1':
        mass_type.append(2)
    elif atoms[i] == 'HW2':
        mass_type.append(2)
    elif atoms[i][:1] == 'O':
        mass_type.append(3)
    elif atoms[i][:1] == 'C':
        mass_type.append(4)
    elif atoms[i][:1] == 'H':
        mass_type.append(5)

ads_atoms, ads_charge = [], []
with open('charge') as f:
    for line in f:
        p = line.split()
        if len(p) == 8:
            ads_atoms.append(p[4])
            ads_charge.append(p[6])
            
CHARGE = pd.DataFrame({'atoms':ads_atoms,'charges':ads_charge})


charges = []
for atom in atoms:
    if atom == 'OW':
        charges.append(-1.1128)
    elif atom in {'HW1', 'HW2'}:
        charges.append(0.5564)
    else:
        if atom in CHARGE['atoms'].values:
            charges.append(float(CHARGE.loc[CHARGE['atoms'] == atom, 'charges'].values[0]))
        else:
            print(f"Warning: Charge for atom '{atom}' not found in CHARGE.")


################ initial information of the simulation ###########################

print("Generated LAMMPS input file by AL from Ashbaugh's group")
print(f"{(numadso+3*numWater):<5} {'atoms':<5}")
print(f"{numbonds:<5} {'bonds':<5}")
print(f"{numangles:<5} {'angles':<5}")
print(f"{numdihedrals:<5} {'dihedrals':<5}")
print(f"{numimpropers:<5} {'impropers':<5}")
print(f"{numatomType:<5} {'atom types':<5}")
print(f"{numbondType:<5} {'bond types':<5}")
print(f"{numangleType:<5} {'angle types':<5}")
print(f"{numdihedralsType:<5} {'dihedral types':<5}")
print(f"{numimpropersType:<5} {'impropers types':<5}")
print("")
print("")
print(f"{0:<10.8f} {10 * lx:<10.8f} {'xlo':<5} {'xhi':<5}")
print(f"{0:<10.8f} {10 * ly:<10.8f} {'ylo':<5} {'yhi':<5}")
print(f"{0:<10.8f} {10 * lz:<10.8f} {'zlo':<5} {'zhi':<5}")
print("")
print("")
print("Bond Coeffs")
print("")
data = []
with open('bonds_coeff') as f:
    for line in f:
        p = line.split()
        data.append([float(x) if '.' in x else int(x) for x in p])

DATA = []
for i in range(len(data)):
    if len(data[i]) > 0:
        DATA.append(data[i])

df = pd.DataFrame(DATA, columns=["type", "K", "r0"])


print(f"{1:<8}{'morse':<8} {103.3893403:<8} {2.287:<8} {0.9419:<8}{'# Hw_Ow':<5}")
for i in range(len(df['r0'])):
    print(f"{int(df['type'][i])+1:<8}{'harmonic':<9}{df['K'][i]:<8} {df['r0'][i]:<8}") 




print("")
print("")
print("Angle Coeffs")
print("")
data = []
with open('angles_coeff') as f:
    for line in f:
        p = line.split()
        data.append([float(x) if '.' in x else int(x) for x in p])
DATA = []
for i in range(len(data)):
    if len(data[i]) > 0:
        DATA.append(data[i])
df = pd.DataFrame(DATA, columns=["type", "K", "teta0"])

print(f"{1:<5} {43.9543499:<8} {107.4:<8} {'# Hw_Ow_Hw':<5}")
for i in range(len(df['teta0'])):
    print(f"{int(df['type'][i])+1:<5} {df['K'][i]:<8} {df['teta0'][i]:<8}") 



print("")
print("")
print("Dihedral Coeffs")
print("")

data = []
with open('dihedral_coeffs') as f:
    for line in f:
        p = line.split()
        data.append([float(x) if '.' in x else int(x) for x in p])
DATA = []
for i in range(len(data)):
    if len(data[i]) > 0:
        DATA.append(data[i])
df = pd.DataFrame(DATA, columns=["type", "V1", "V2", "V3", "V4"])
for i in range(len(df['type'])):
    print(f"{df['type'][i]:<5} {df['V1'][i]:<8} {df['V2'][i]:<8} {df['V3'][i]:<8}{df['V4'][i]:<8}") 

print("")
print("")
print("Improper Coeffs")
print("")
data = []
with open('improper_coeffs') as f:
    for line in f:
        p = line.split()
        data.append([float(x) if '.' in x else int(x) for x in p])
DATA = []
for i in range(len(data)):
    if len(data[i]) > 0:
        DATA.append(data[i])
df = pd.DataFrame(DATA, columns=["type", "K", "d", "n"])
for i in range(len(df['type'])):
    print(f"{df['type'][i]:<5} {df['K'][i]:<8} {df['d'][i]:<8} {df['n'][i]:<8}")




print("")
print("")
print("Masses")
print("")
print(f"{1:<5} {Mw_Ow:<5} {'#Ow':<5}")
print(f"{2:<5} {Mw_Hw:<5} {'#Hw':<5}")
print(f"{3:<5} {Mw_Ow:<5} {'#O':<5}")
print(f"{4:<5} {Mw_C:<7} {'#C':<5}")
print(f"{5:<5} {Mw_Hw:<5} {'#H':<5}")

print("")
print("Atoms")
print("")


for i in range(len(atoms)):
    print(f"{index[i]:<3} {molecule_id[i]:<3} {mass_type[i]:<3} {charges[i]:<10} {x[i]:<10.6f} {y[i]:<10.6f} {z[i]:<10.6f} {names[i]}")
    

print("")
print("Bonds")
print("")
count = 0
for i in range(0,numWater*3,3):
    for j in range(1,3):
        count += 1
        print(f"{count:<5} {'1':<5} {index[i]:<5} {index[i+j]:<5}")

ads_INDEX = index[numWater*3:len(atoms)]
data = []
with open('bonds') as f:
    for line in f:
        p = line.split()
        data.append([float(x) if '.' in x else int(x) for x in p])
DATA = []
for i in range(len(data)):
    if len(data[i]) > 0:
        DATA.append(data[i])
df = pd.DataFrame(DATA, columns=["index", "type", "I", "J"])


replacement_map = {
    1: ads_INDEX[0],
    2: ads_INDEX[1],
    3: ads_INDEX[2],
    4: ads_INDEX[3],
    5: ads_INDEX[4],
    6: ads_INDEX[5],
    7: ads_INDEX[6],
    8: ads_INDEX[7],
    9: ads_INDEX[8],
    10: ads_INDEX[9],
    11: ads_INDEX[10],
    12: ads_INDEX[11],
    13: ads_INDEX[12],
    14: ads_INDEX[13]
}

df['I'] = df['I'].map(replacement_map).astype(int)
df['J'] = df['J'].map(replacement_map).astype(int)
countt = 1
for i in range(len(df['index'])): 
    count +=1
    countt +=1
    print(f"{count:<5} {countt:<5}{df['I'][i]:<5}{df['J'][i]:<5}")

print("")
print("Angles")
print("")
typeangle = 1
count = 0
for i in range(0,numWater*3,3):
    count +=1
    print(f"{count:<5} {typeangle:<5} {index[i+1]:<5} {index[i]:<5} {index[i+2]:<5}")



data = []
with open('angles') as f:
    for line in f:
        p = line.split()
        
        data.append([float(x) if '.' in x else int(x) for x in p])

DATA = []
for i in range(len(data)):
    if len(data[i]) > 0:
        DATA.append(data[i])


df = pd.DataFrame(DATA, columns=["index","type","I", "J", "K"])


df['I'] = df['I'].map(replacement_map).astype(int)
df['J'] = df['J'].map(replacement_map).astype(int)
df['K'] = df['K'].map(replacement_map).astype(int)

typeangle = 1
for i in range(len(df['index'])):
    count+=1
    typeangle+=1
    print(f"{count:<5} {typeangle:<5} {df['I'][i]:<5} {df['J'][i]:<5} {df['K'][i]:<5}")
print("")
print("Dihedrals")
print("")
data = []

# Read and process the file
with open('dihedrals-proper') as f:
    for line in f:
        p = line.split()
        # Convert each element to float or int if needed
        data.append([float(x) if '.' in x else int(x) for x in p])

DATA = []
for i in range(len(data)):
    if len(data[i]) > 0:
        DATA.append(data[i])
        


# Convert data to DataFrame
df = pd.DataFrame(DATA, columns=["index","type","I", "J", "K", "L"])
# # Replace values in Col1, Col2, and Col3 using the replacement map
df['I'] = df['I'].map(replacement_map).astype(int)
df['J'] = df['J'].map(replacement_map).astype(int)
df['K'] = df['K'].map(replacement_map).astype(int)
df['L'] = df['L'].map(replacement_map).astype(int)
count = 0
for i in range(len(df['index'])):
    count+=1    
    print(f"{count:<5} {count:<5} {df['I'][i]:<5} {df['J'][i]:<5} {df['K'][i]:<5}{df['L'][i]:<5}")


print("")
print("Impropers")
print("")
data = []
with open('dihedrals-improper') as f:
    for line in f:
        p = line.split()
        # Convert each element to float or int if needed
        data.append([float(x) if '.' in x else int(x) for x in p])

DATA = []
for i in range(len(data)):
    if len(data[i]) > 0:
        DATA.append(data[i])

df = pd.DataFrame(DATA, columns=["index","type","I", "J", "K", "L"])
# # Replace values in Col1, Col2, and Col3 using the replacement map
df['I'] = df['I'].map(replacement_map).astype(int)
df['J'] = df['J'].map(replacement_map).astype(int)
df['K'] = df['K'].map(replacement_map).astype(int)
df['L'] = df['L'].map(replacement_map).astype(int)


count = 0
for i in range(len(df['index'])):
    count+=1
    print(f"{count:<5} {count:<5} {df['I'][i]:<5} {df['J'][i]:<5} {df['K'][i]:<5}{df['L'][i]:<5}")
