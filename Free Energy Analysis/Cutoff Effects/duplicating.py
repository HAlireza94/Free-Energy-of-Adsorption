
atoms, x, y, z = [], [], [], []
nx, ny = 3, 3 # duplicating factors
with open('conf.gro') as f:
    for line in f:
        p = line.split()
        
        if len(p) == 9:
            atoms.append(p[1])
            x.append(float(p[3]))
            y.append(float(p[4]))
            z.append(float(p[5]))
        if len(p) == 3:
            Lx = float(p[0])
            Ly = float(p[1])
            Lz = float(p[2])

# all units are in nm
X, Y, Z, = [], [], []

for i in range(nx):
    if i == 0:
        X.append(x)
        Y.append(y)
        Z.append(z)
    else:
        x1 = []
        y1 = []
        z1 = []
        for j in range(len(X[0])):
            x1.append(X[i-1][j]+Lx)
            y1.append(Y[0][j])
            z1.append(Z[0][j])
        X.append(x1)
        Y.append(y1)
        Z.append(z1)


if ny >=2:
    for i in range(1,ny):
       
        for k in range(nx):
            x1, y1, z1 = [], [], []
            for j in range(len(X[0])):
                x1.append(X[k][j])
                y1.append(Y[k][j]+ i*Ly)
                z1.append(Z[0][j])
            X.append(x1)
            Y.append(y1)
            Z.append(z1)
            print(len(X))


ATOMS = []
for i in range(nx*ny):
    ATOMS.append(atoms)


filename = f"new-system.xyz"
with open(filename, 'w') as file:
    file.write(str(nx*ny*len(X[0])) + '\n')
    file.write('system' + '\n')
    for i in range(nx*ny):
        for j in range(len(X[0])):
            file.write(f"{ATOMS[i][j]:<6}{X[i][j]*10:<14.5f}{Y[i][j]*10:<14.5f}{Z[i][j]*10:<14.5f}\n") # converting to Angstrom
        
Lx = Lx * nx * 10
Ly = Ly * ny * 10
filename = f"new-system.pdb"
with open(filename, 'w') as file:
    file.write("REMARK    bx = {}  by = {}  bz = {}\n".format(Lx, Ly, Lz))
    file.write("REMARK    # of atoms = {}\n".format(nx*ny*len(X[0])))
    ss = 0
    for i in range(nx*ny):
        for j in range(len(X[0])):
            ss += 1
            sym_at = "ATOM"
            xyz = "XYZ"
            file.write("ATOM{:>6}  {:<3}  XYZ{:>6}    {:8.3f}{:8.3f}{:8.3f}\n".format(ss, ATOMS[i][j], 1, X[i][j]*10, Y[i][j]*10, Z[i][j]*10))


