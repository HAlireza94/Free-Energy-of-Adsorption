import pandas as pd
import numpy as np

Lx, Ly, Lz = 1.1098000000000001e+01, 1.4417000000000000e+01, 5.0000000000000000e+01  

numWater = 40
numadso = 96
totalParticles = 3*numWater + numadso
index, atoms, x, y, z = [], [], [], [], []
with open('dump.Pt_clean_NVE.lammpstrj') as f:
    for line in f:
        p = line.split()
        if len(p) == 8:
            index.append(int(p[0]))
            atoms.append(p[1])
            x.append(float(p[5]))
            y.append(float(p[6]))
            z.append(float(p[7]))

df = pd.DataFrame({'idx':index,'atoms':atoms,'x':x,'y':y,'z':z})
numFrames = len(df['idx']) // totalParticles

def apply_pbc(coord1, coord2, L):
    delta = abs(coord1 - coord2)
    if delta > L / 2.0:
        delta = L - delta
    return delta

av_b = 0
av_teta = 0
for i in range(numFrames):
    data = df[totalParticles*i:(i+1)*totalParticles]
    df_water = data[numadso:numWater*3 + numadso].reset_index()
    av_bb = 0
    av_tt = 0
    for j in range(0, len(df_water['idx']), 3):
        B = 0
        for k in range(1, 3):
            dx = apply_pbc(df_water['x'][j], df_water['x'][j+k], Lx)
            dy = apply_pbc(df_water['y'][j], df_water['y'][j+k], Ly)
            dz = apply_pbc(df_water['z'][j], df_water['z'][j+k], Lz)
            b = (dx**2 + dy**2 + dz**2)**0.5
            B += b
        av_bb += B
    av_b += av_bb
        


print('<O-H> = ' + str(np.round(av_b/numFrames/(numWater*2),4)))

av_t = 0
for i in range(numFrames):
    data = df[totalParticles*i:(i+1)*totalParticles]
    df_water = data[numadso:numWater*3 + numadso].reset_index()
    av_tt = 0
    for j in range(0, len(df_water['idx']), 3):
        O=[df_water['x'][j], df_water['y'][j], df_water['z'][j]]
        H1=[df_water['x'][j+1], df_water['y'][j+1], df_water['z'][j+1]]
        H2=[df_water['x'][j+2], df_water['y'][j+2], df_water['z'][j+2]]

        V1 = [apply_pbc(H1[0],O[0], Lx),apply_pbc(H1[1],O[1], Ly),apply_pbc(H1[2],O[2], Lz)]
        V2 = [apply_pbc(H2[0],O[0], Lx),apply_pbc(H2[1],O[1], Ly),apply_pbc(H2[2],O[2], Lz)]

        # V1=[H1[0]-O[0],H1[1]-O[1],H1[2]-O[2]]
        # V2=[H2[0]-O[0],H2[1]-O[1],H2[2]-O[2]]

        V1V2 = V1[0]*V2[0] + V1[1]*V2[1] + V1[2]*V2[2]
        L_V1 = np.sqrt(V1[0]**2 + V1[1]**2 + V1[2]**2)  # Magnitude of V1
        L_V2 = np.sqrt(V2[0]**2 + V2[1]**2 + V2[2]**2)  # Magnitude of V2

        cos_theta1 = V1V2 / (L_V1 * L_V2)

        av_tt += (np.rad2deg(np.arccos(cos_theta)))
    av_t += av_tt



print('<H1-O-H2> = ' + str(np.round(av_t/numFrames/numWater,4)))