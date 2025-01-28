numPt = 64
numWater = 40 
numbonds = numWater*2
numangles = numWater

Mw_Hw = 1.007940
Mw_Ow = 15.999400
Mw_Pt = 102.90500

numdihedrals = 0
numimpropers = 0
numatomType = 3
numbondType = 1
numangleType = 1
numdihedralsType = 0
numimpropersType = 0

Pt_masstype = 3


## default charge for Pt is zero unless they are provided from DFT
chargesPt = []
with open('data') as f:
    for line in f:
        p = line.split()
        if len(p)==5 and p[0] != 'atoms':
            chargesPt.append(float(p[4]))




typeAPt = []
for i in range(numPt):
    typeAPt.append(1)

typeAh2o = []
f = 1
for i in range(numPt,3*numWater+numPt,3):
    f+=1
    for j in range(3):
        typeAh2o.append(f)



Pt_masstype = []
for i in range(numPt):
    Pt_masstype.append(3)


water_masstype=[] ## OW is 1 and HW is 2 so it is 1 2 2 repeated for all water molecules

for i in range(numPt,numPt+3*numWater,3):
    k = 1
    for j in range(3):
        k+=j
        if k == 4:
            water_masstype.append(2)
        else:
            water_masstype.append(k)
chargesWater = []

for i in range(len(water_masstype)):
    if water_masstype[i] == 1:
        chargesWater.append(-0.834)
    elif water_masstype[i] == 2:
        chargesWater.append(0.417)

        
    


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


################ initial information of the simulation ###########################

print("Generated LAMMPS input file by AL from Ashbaugh's group")
print(f"{(numPt+3*numWater):<5} {'atoms':<5}")
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
print(f"{1:<5} {450.0:<5} {0.9572:<5} {'# Hw_Ow':<5}")
print("")
print("")
print("Angle Coeffs")
print("")
print(f"{1:<5} {55.00:<5} {104.52:<5} {'# Hw_Ow_Hw':<5}")
print("")
print("")
print("Masses")
print("")
print(f"{1:<5} {Mw_Ow:<5} {'#Ow':<5}")
print(f"{2:<5} {Mw_Hw:<5} {'#Hw':<5}")
print(f"{3:<5} {Mw_Pt:<5} {'#Pt':<5}")


#index,typA,masstype,chargesPt,x,y,z,NAMES

print("")
print("Atoms")
print("")


for i in range(numPt):
    print(f"{index[i]:<3} {typeAPt[i]:<3} {Pt_masstype[i]:<3} {chargesPt[i]:<10.6f} {x[i]:<10.6f} {y[i]:<10.6f} {z[i]:<10.6f} {Names[i]}")



index = index[numPt:numPt+3*numWater]
#typeA = typeA[numPt:numPt+3*numWater]
x = x[numPt:numPt+3*numWater]
y = y[numPt:numPt+3*numWater]
z = z[numPt:numPt+3*numWater]
Names = Names[numPt:numPt+3*numWater]


for i in range(len(typeAh2o)):    
    print(f"{index[i]:<3} {typeAh2o[i]:<3} {water_masstype[i]:<3} {chargesWater[i]:<10.6f} {x[i]:<10.6f} {y[i]:<10.6f} {z[i]:<10.6f} {Names[i]}")

## index, typebond, i, j **** typebond should be 1 indicating harmonic
typebond = 1
count = 0

print("")
print("Bonds")
print("")

for i in range(0,len(index),3):
    
    for j in range(1,3):
        count += 1
        print(f"{count:<5} {typebond:<5} {index[i]:<5} {index[i+j]:<5}")

print("")
print("Angles")
print("")


## index, typeangle, i, j, k **** typeangle should be 1 indicating harmonic
count = 0
typeangle = 1
for i in range(0,len(index),3):
    count +=1
    print(f"{count:<5} {typeangle:<5} {index[i+1]:<5} {index[i]:<5} {index[i+2]:<5}")
    


