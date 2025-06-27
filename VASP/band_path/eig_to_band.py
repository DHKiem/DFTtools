# this code is written to convert EIGENVAL to BAND.dat when using explicit kpoints.
# DHK
# date: 2025-Jun

import numpy as np
from numpy import linalg as LA



# read POSCAR, EIGENVAL, and KPOINTS(explicit kpoints)


#EIGENVAL
with open("EIGENVAL", "r") as f:
    lines = f.readlines()
nk = int(lines[5].split()[1])
nbands = int(lines[5].split()[2])    

with open("POSCAR", "r") as f:
    lineposcar = f.readlines()

#with open("KPOINTS", "r") as f:
    #linek = f.readlines()    
linek = np.loadtxt("KPOINTS",skiprows =3)

#print(linek)

Ra=np.array(lineposcar[2].split()[0:3]).astype(np.float64)
Rb=np.array(lineposcar[3].split()[0:3]).astype(np.float64)
Rc=np.array(lineposcar[4].split()[0:3]).astype(np.float64)

Ga = 2*np.pi * np.cross(Rb, Rc)/ np.dot(Ra,np.cross(Rb,Rc))
Gb = 2*np.pi * np.cross(Rc, Ra)/ np.dot(Ra,np.cross(Rb,Rc))
Gc = 2*np.pi * np.cross(Ra, Rb)/ np.dot(Ra,np.cross(Rb,Rc))

def read_kpaths_with_ngrid(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()

    kpaths = []

    i = 4  # skip first 4 header lines
    while i < len(lines):
        # Skip blank lines
        if lines[i].strip() == "":
            i += 1
            continue

        # Start point line
        parts_start = lines[i].split()
        start_k = list(map(float, parts_start[:3]))
        i += 1

        while i < len(lines) and lines[i].strip() == "":
            i += 1
        if i >= len(lines):
            break

        # End point line
        parts_end = lines[i].split()
        end_k = list(map(float, parts_end[:3]))

        # Default to -1; optionally modify this based on segment length or external logic
        kpaths.append([-1, start_k, end_k])
        i += 1

    return kpaths
#print(read_kpaths_with_ngrid("KPATH.in"))
kpaths = read_kpaths_with_ngrid("KPATH.in")

kpath_list = []
pathlength_list = []
for klist in kpaths:
    pathdiff = np.array(klist[2]) - np.array(klist[1])
    pathlength = LA.norm(pathdiff[0]*Ga + pathdiff[1]*Gb + pathdiff[2]*Gc)
    pathlength_list.append(pathlength)
length_total = sum(pathlength_list)
kn_list = np.round(np.array(pathlength_list) / (length_total / nk)).astype(int)


[50, 25, 15, 29, 28, 13, 41]
for ki, nnk in enumerate(kn_list):
    kpaths[ki][0] = nnk
#kpaths = [
#    [50,  [  0.0000000000 ,  0.0000000000 ,  0.0000000000],[  0.5000000000 ,  0.5000000000 ,  0.5000000000   ]],
#    [25,  [  0.5000000000 ,  0.5000000000 ,  0.5000000000],[  0.8113023911 ,  0.1886976089 ,  0.5000000000   ]],
#    [15,  [ 0.5000000000  ,-0.1886976089  , 0.1886976089 ],[ 0.5000000000  , 0.0000000000  , 0.0000000000    ]],
#    [29,  [ 0.5000000000  , 0.0000000000  , 0.0000000000 ],[ 0.0000000000  , 0.0000000000  , 0.0000000000    ]],
#    [28,  [ 0.0000000000  , 0.0000000000  , 0.0000000000 ],[ 0.3443488044  ,-0.3443488044  , 0.0000000000    ]],
#    [13,  [ 0.6556511956  , 0.0000000000  , 0.3443488044 ],[ 0.5000000000  , 0.0000000000  , 0.5000000000    ]],
#    [41,  [ 0.5000000000  , 0.0000000000  , 0.5000000000 ],[ 0.0000000000  , 0.0000000000  , 0.0000000000    ]],
#]


nk_user = sum([kpaths[i][0] for i in range(len(kpaths))])
print(sum([kpaths[i][0] for i in range(len(kpaths))])  )

assert(nk == nk_user)

print(f"Number of Kpoints: {nk}")
print(f"Number of bands: {nbands}")

assert(len(lines) == 8 + (nbands+2)*nk -2)
#print(len(lines), 8 + (nbands+2)*nk -2)

spin_type = 1 * (len(lines[8].split()) == 3) + 2* (len(lines[8].split()) == 5) # 1 for NM|NCL, 2 for COL
print("spin type: ",spin_type)

klengths = np.zeros(nk)

# from KPOINTS (but cannot find the end of each path)
#for ki in range(1,nk):
#    tempk= np.array(linek[ki]) - np.array(linek[ki-1])
#    klengths[ki] = LA.norm(tempk[0]*Ga + tempk[1]*Gb + tempk[2]*Gc) + klengths[ki-1]
    
# from kpaths manually inserted
for (pathidx, each_path) in enumerate(kpaths):
    ngrid = each_path[0]
    kdistance_frac = (np.array(each_path[2]) - np.array(each_path[1]))/(ngrid-1)
    kdistance_cart = LA.norm(kdistance_frac[0]*Ga + kdistance_frac[1]*Gb + kdistance_frac[2]*Gc)
    startidx = sum([kpaths[i][0] for i in range(pathidx)])
    print(startidx," ", kdistance_cart)

    for ik in range(ngrid):
        idx = ik + startidx
        
        if idx != 0:
            klengths[idx] = klengths[startidx-1] + kdistance_cart*ik
        

with open("BAND.dat", "w") as f:
    for bandidx in range(nbands):
        #print("# Band-Index:    ",bandidx+1)
        for ki in range(nk):
            blockidx = 8+ki*(nbands+2)
            bandline = blockidx + bandidx
            assert(int(lines[bandline].split()[0]) == bandidx+1)

            if spin_type == 1:
                eigenval = lines[bandline].split()[1]
                #print(f"{klengths[ki]: <10} {eigenval: <10}")
                f.write(f"{klengths[ki]: <10} {eigenval: <10}\n")
            if spin_type == 2:
                eigenval1 = lines[bandline].split()[1]
                eigenval2 = lines[bandline].split()[2]
                #print(f"{klengths[ki]: <10} {eigenval1: <10} {eigenval2: <10}")
                f.write(f"{klengths[ki]: <10} {eigenval1: <10} {eigenval2: <10}\n")
        f.write("\n")
        
    
    

'''
for ki in range(nk):
    startidx = 8+ki*(nbands+2)
    endidx = startidx + nbands
    print("# Band-Index:    ")
    if spin_type ==1 :
        for li in range(startidx,endidx,1):
            print(f"{lines[li].split()[0]: <10}  {lines[li].split()[1]: <10}")
    if spin_type ==2 :
        for li in range(startidx,endidx,1):
            print(f"{lines[li].split()[0]: <10}  {lines[li].split()[1]: <10}  {lines[li].split()[2]: <10}")
    print(" ")
                  
'''
    #print(    lines[startidx:endidx])

