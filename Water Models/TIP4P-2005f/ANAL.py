import numpy as np
idx = ['1','2','3','4']
idx1_x, idx2_x, idx3_x, idx4_x = [], [], [], []
idx1_y, idx2_y, idx3_y, idx4_y = [], [], [], []
idx1_z, idx2_z, idx3_z, idx4_z = [], [], [], []
with open('checking.gro') as f:
    for line in f:
        p = line.split()
        if len(p) == 6:
            if p[2] == idx[0]:
                idx1_x.append(float(p[3]))
                idx1_y.append(float(p[4]))
                idx1_z.append(float(p[5]))
            elif p[2] == idx[1]:
                idx2_x.append(float(p[3]))
                idx2_y.append(float(p[4]))
                idx2_z.append(float(p[5]))
            elif p[2] == idx[2]:
                idx3_x.append(float(p[3]))
                idx3_y.append(float(p[4]))
                idx3_z.append(float(p[5]))
            elif p[2] == idx[3]:
                idx4_x.append(float(p[3]))
                idx4_y.append(float(p[4]))
                idx4_z.append(float(p[5]))
                
frames = len(idx1_x)
print(str(frames) + " " + "frames have been processed")

av_angle = 0
av_r_oh = 0
av_r_om = 0
for i in range(frames):
    V1 = [idx2_x[i]-idx1_x[i],idx2_y[i]-idx1_y[i],idx2_z[i]-idx1_z[i]]
    V2 = [idx3_x[i]-idx1_x[i],idx3_y[i]-idx1_y[i],idx3_z[i]-idx1_z[i]]
    V3 = [idx4_x[i]-idx1_x[i],idx4_y[i]-idx1_y[i],idx4_z[i]-idx1_z[i]]
    V1V2 = V1[0]*V2[0] + V1[1]*V2[1] + V1[2]*V2[2]
    L_V1 = np.sqrt(V1[0]**2 + V1[1]**2 + V1[2]**2)
    L_V2 = np.sqrt(V2[0]**2 + V2[1]**2 + V2[2]**2)
    L_V3 = np.sqrt(V3[0]**2 + V3[1]**2 + V3[2]**2)
    teta = np.rad2deg(np.arccos(V1V2/(L_V1*L_V2)))
    av_angle += teta/frames
    av_r_oh += 10 * L_V1/frames 
    av_r_om += 10 * L_V3/frames

print(f"{'<teta> = ':<6}{av_angle:<6.4f}")
print(f"{'<r_OH> = ':<6}{av_r_oh:<6.4f} {' A'}")
print(f"{'<d_OM> = ':<6}{av_r_om:<6.4f} {' A'}")
