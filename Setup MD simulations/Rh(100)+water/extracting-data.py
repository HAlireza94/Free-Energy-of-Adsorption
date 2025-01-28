import re

element = 'Rh'
atom,x,y,z,charge = [], [], [], [], []
with open('DDEC6.xyz') as f:
    for line in f:
        p=line.split()
        
        if len(p) == 5:
            if p[0] == element:
                atom.append(p[0])
                x.append(p[1])
                y.append(p[2])
                z.append(p[3])
                charge.append(p[4])
        
        if len(p)==24:
            if p[0] == 'jmolscript:':
                pattern = r"unitcell \[\{(.+?)\}\]"
                match = re.search(pattern, line)
                if match:
                    unitcell_data = match.group(1)
                    vectors = [list(map(float, re.findall(r"-?\d+\.\d+", vec))) for vec in unitcell_data.split('}, {')]
                    bx, by, bz = vectors[0][0], vectors[1][1], vectors[2][2]
                    
                else:
                    print("Unit cell data not found.")


print(len(atom))
print(f"{'atoms':<10}{'X':<5}{'Y':<5}{'Z':<5}{'Charge':<5}")
print("")
for i in range(len(x)):
    print(f"{atom[i]:<10}{x[i]:<10}{y[i]:<10}{z[i]:<10}{charge[i]:<10}")

print("")
print(f"{'boxSize':<15}{bx:<15}{by:<15}{bz:<15}")
