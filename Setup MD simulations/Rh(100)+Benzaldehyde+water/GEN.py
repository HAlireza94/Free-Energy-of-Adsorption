import numpy as np
import pandas as pd

numadso = 14
numRh = 64
numWater = 40 
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
numatomType = 6
numbondType = 6
numangleType = 5
numdihedralsType = 3
numimpropersType = 2

Rh_masstype = 3



## default charge for Pt is zero unless they are provided from DFT
charges_Rh_ad = []
with open('data') as f:
    for line in f:
        p = line.split()
        if len(p)==5 and p[0] != 'atoms':
            charges_Rh_ad.append(float(p[4]))




typeAPt = []
for i in range(numRh+numadso):
    
    if int(i) >=numRh:
        typeAPt.append(2)
    else:
        typeAPt.append(1)


typeAh2o = []
f = 2
for i in range(numRh+numadso,3*numWater+numRh+numadso,3):
    f+=1
    for j in range(3):
        typeAh2o.append(f)







        
names, index, x, y, z = [], [], [], [], []

with open ('conf.gro') as f:
    for line in f:
        p = line.split()
        if len(p) == 9:
            names.append(p[1])
            index.append(p[2])
            x.append(float(p[3])*10)
            y.append(float(p[4])*10)
            z.append(float(p[5])*10)
        elif len(p) == 3:
            lx = float(p[0])
            ly = float(p[1])
            lz = float(p[2])


Names = []
for i in range(len(names)):
    Names.append("#"+names[i]) 


mass_type = []
for i in range(len(names)):
    if names[i] == 'RH':
        mass_type.append(3)
    elif names[i] == 'OW':
        mass_type.append(1)
    elif names[i] == 'HW1':
        mass_type.append(2)
    elif names[i] == 'HW2':
        mass_type.append(2)
    elif names[i] == 'O':
        mass_type.append(4)
    elif names[i] == 'C':
        mass_type.append(5)
    elif names[i] == 'H':
        mass_type.append(6)
    






################ initial information of the simulation ###########################

print("Generated LAMMPS input file by AL from Ashbaugh's group")
print(f"{(numRh+numadso+3*numWater):<5} {'atoms':<5}")
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
for i in range(len(df['r0'])):
    print(f"{df['type'][i]:<5} {df['K'][i]:<8} {df['r0'][i]:<8}") 


print(f"{int(df['type'][len(df['type'])-1])+1:<5} {450.0:<8} {0.9572:<8} {'# Hw_Ow':<5}")

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
for i in range(len(df['teta0'])):
    print(f"{df['type'][i]:<5} {df['K'][i]:<8} {df['teta0'][i]:<8}") 
print(f"{int(df['type'][len(df['type'])-1])+1:<5} {55.00:<8} {104.52:<8} {'# Hw_Ow_Hw':<5}")


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
print(f"{3:<5} {Mw_Rh:<5} {'#Rh':<5}")
print(f"{4:<5} {Mw_Ow:<5} {'#O':<5}")
print(f"{5:<5} {Mw_C:<7} {'#C':<5}")
print(f"{6:<5} {Mw_Hw:<5} {'#H':<5}")

#index,typA,masstype,chargesPt,x,y,z,NAMES

print("")
print("Atoms")
print("")

# sheet
for i in range(numRh):
    print(f"{index[i]:<3} {typeAPt[i]:<3} {mass_type[i]:<3} {charges_Rh_ad[i]:<10.6f} {x[i]:<10.6f} {y[i]:<10.6f} {z[i]:<10.6f} {Names[i]}")

# adsorbate
for i in range(numRh,numRh+numadso):
    print(f"{index[i]:<3} {typeAPt[i]:<3} {mass_type[i]:<3} {charges_Rh_ad[i]:<10.6f} {x[i]:<10.6f} {y[i]:<10.6f} {z[i]:<10.6f} {Names[i]}")
# water

index = index[numRh+numadso:numRh+numadso+3*numWater]
#typeA = typeA[numPt:numPt+3*numWater]
x = x[numRh+numadso:numRh+numadso+3*numWater]
y = y[numRh+numadso:numRh+numadso+3*numWater]
z = z[numRh+numadso:numRh+numadso+3*numWater]
Names = Names[numRh+numadso:numRh+numadso+3*numWater]
water_masstype = mass_type[numRh+numadso:numRh+numadso+3*numWater]

chargesWater = []
for i in range(numWater*3):
    if water_masstype[i] == 1:
        chargesWater.append(-0.834)
    elif water_masstype[i] == 2:
        chargesWater.append(0.417)


for i in range(len(typeAh2o)):    
    print(f"{index[i]:<3} {typeAh2o[i]:<3} {water_masstype[i]:<3} {chargesWater[i]:<10.6f} {x[i]:<10.6f} {y[i]:<10.6f} {z[i]:<10.6f} {Names[i]}")

## index, typebond, i, j **** typebond should be 1 indicating harmonic
## bonds for adsorbate

print("")
print("Bonds")
print("")

data = []
with open('bonds') as f:
    for line in f:
        p = line.split()
        # Convert each element to float or int if needed
        data.append([float(x) if '.' in x else int(x) for x in p])

# Mapping for replacements
replacement_map = {
    1: 65,
    2: 72,
    3: 66,
    4: 68,
    5: 70,
    6: 71,
    7: 69,
    8: 67,
    9: 78,
    10: 74,
    11: 76,
    12: 77,
    13: 75,
    14: 73
}


DATA = []
for i in range(len(data)):
    if len(data[i]) > 0:
        DATA.append(data[i])

df = pd.DataFrame(DATA, columns=["I", "J", "func", "r0", "K"])

df['I'] = df['I'].map(replacement_map).astype(int)
df['J'] = df['J'].map(replacement_map).astype(int)


count = 0
countt = 0
for i in range(len(df['r0'])): 
    count +=1
    countt +=1
    print(f"{count:<5} {countt:<5}{df['I'][i]:<5}{df['J'][i]:<5}")
                
            



typebond = countt+1
for i in range(0,len(index),3):
    
    for j in range(1,3):
        count += 1
        print(f"{count:<5} {typebond:<5} {index[i]:<5} {index[i+j]:<5}")



## index, typebond, i, j **** typebond should be 1 indicating harmonic

print("")
print("Angles")
print("")

## index, typeangle, i, j, k **** typeangle should be 1 indicating harmonic
count = 0
data = []
with open('angles') as f:
    for line in f:
        p = line.split()
        # Convert each element to float or int if needed
        data.append([float(x) if '.' in x else int(x) for x in p])

DATA = []
for i in range(len(data)):
    if len(data[i]) > 0:
        DATA.append(data[i])

# Convert data to DataFrame
df = pd.DataFrame(DATA, columns=["I", "J", "K", "col4", "col5", "col6"])

# Replace values in Col1, Col2, and Col3 using the replacement map
df['I'] = df['I'].map(replacement_map).astype(int)
df['J'] = df['J'].map(replacement_map).astype(int)
df['K'] = df['K'].map(replacement_map).astype(int)

# Display the updated DataFrame
# print(df)
countt = 0
for i in range(len(df['I'])):
    count+=1
    countt+=1
        
    print(f"{count:<5} {countt:<5} {df['I'][i]:<5} {df['J'][i]:<5} {df['K'][i]:<5}")

typeangle = countt+1
for i in range(0,len(index),3):
    count +=1
    print(f"{count:<5} {typeangle:<5} {index[i+1]:<5} {index[i]:<5} {index[i+2]:<5}")


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
df = pd.DataFrame(DATA, columns=["I", "J", "K", "L", "func", "c0", "c1", "c2", "c3", "c4", "c5"])
# # Replace values in Col1, Col2, and Col3 using the replacement map
df['I'] = df['I'].map(replacement_map).astype(int)
df['J'] = df['J'].map(replacement_map).astype(int)
df['K'] = df['K'].map(replacement_map).astype(int)
df['L'] = df['L'].map(replacement_map).astype(int)

count = 0
for i in range(len(df['I'])):
    count+=1
    if df['c0'][i] == 8.786 and df['c1'][i] == 0.0 and df['c2'][i] == -8.786:
        typeDihP = 1
    elif df['c0'][i] == 30.334 and df['c1'][i] == 0.0 and df['c2'][i] == -30.334:
        typeDihP = 2
    elif df['c0'][i] == 0.837 and df['c1'][i] == 0.0 and df['c2'][i] == -0.837:
        typeDihP = 3
    
    
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

df = pd.DataFrame(DATA, columns=["I", "J", "K", "L", "func", "zita(degree)", "K-zita", "multiplicity"])
# # Replace values in Col1, Col2, and Col3 using the replacement map
df['I'] = df['I'].map(replacement_map).astype(int)
df['J'] = df['J'].map(replacement_map).astype(int)
df['K'] = df['K'].map(replacement_map).astype(int)
df['L'] = df['L'].map(replacement_map).astype(int)


count = 0
for i in range(len(df['I'])):
    count+=1
    if df['zita(degree)'][i] == 180.0 and df['K-zita'][i] == 10.460:
        typeDihI = 1
    elif df['zita(degree)'][i] == 180.0 and df['K-zita'][i] == 43.932:
        typeDihI = 2
    
    print(f"{count:<5} {count:<5} {df['I'][i]:<5} {df['J'][i]:<5} {df['K'][i]:<5}{df['L'][i]:<5}")



