z = []
with open('sheet.gro') as f:
    for line in f:
        p=line.split()
        if len(p) == 6:
            if p[1] == 'RH':
                z.append(float(p[5]))


print(max(z)-min(z))
