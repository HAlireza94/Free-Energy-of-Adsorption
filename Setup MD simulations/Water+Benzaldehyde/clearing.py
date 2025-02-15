import pandas as pd
import numpy as np

atoms, index, x, y, z = [], [], [], [], []
with open('conf.gro') as f:
    for line in f:
        p = line.split()
        if len(p) == 9:
            atoms.append(p[1])
            index.append(p[2])
            x.append(p[3])
            y.append(p[4])
            z.append(p[5])
        elif len(p) == 3:
            lx = float(p[0])
            ly = float(p[1])
            lz = float(p[2])

id_M = []
for i in range(len(atoms)):
    if atoms[i] == 'MW':
        id_M.append(index[i])


df = pd.DataFrame({'ATOMS':atoms,'INDEX':index,'X':x,'Y':y,'Z':z})
f1 = df[~df['INDEX'].isin(id_M)].reset_index(drop=True)

file = 'new-conf.gro'
ix = 0
with open(file,'w') as f:
    f.write("Modifed & cleaned by AL from Ashabugh's group"+'\n')

    for i in range(len(f1['ATOMS'])):
        ix += 1
        f.write("{:<5}{:>5}{:8.3f}{:8.3f}{:8.3f}  {}  {}  {}\n".format(f1['ATOMS'].iloc[i], ix, float(f1['X'].iloc[i]), float(f1['Y'].iloc[i]), float(f1['Z'].iloc[i]), '0.00000', '0.00000', '0.00000'))
        #print(f"{f1['ATOMS'].iloc[i]:<7}{f1['INDEX'].iloc[i]:<7}{f1['X'].iloc[i]:<7}{f1['Y'].iloc[i]:<7}{f1['Z'].iloc[i]:<7}")

    f.write("{:10.5f}{:10.5f}{:10.5f}\n".format(lx,ly,lz))
