


atom,x,y,z = [],[],[],[]
with open('data') as f:
    for line in f:
        p = line.split()

        if len(p) == 5 and p[0] != 'atoms':
            atom.append(p[0])
            x.append(p[1])
            y.append(p[2])
            z.append(p[3])
        

print(len(atom))
print("surface and adsorbate")
for i in range(len(x)):
    print(f"{atom[i]:<10}{x[i]:<10}{y[i]:<10}{z[i]:<10}")

