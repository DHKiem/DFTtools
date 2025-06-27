# Date: 2025-Jun-27

import numpy as np
import sys

# Lattice vectors
with open("POSCAR", "r") as f:
    lineposcar = f.readlines() 
lattice_vec = np.array([
    np.array(lineposcar[i].split()[0:3]).astype(np.float64) for i in range(2,5)
])

# K-paths
def read_kpath(kpathfile):
    with open(kpathfile, 'r') as f:
        lines = f.readlines()
    kpaths = []
    i = 4
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        parts = line.split()
        if len(parts) >= 3:
            start_k = list(map(float, parts[0:3]))
        else:
            raise ValueError(f"Invalid line at {i}: {line}")
        
        i += 1
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        if i >= len(lines):
            break

        parts = lines[i].split()
        if len(parts) >= 3:
            end_k = list(map(float, parts[0:3]))
        else:
            raise ValueError(f"Invalid line at {i}: {lines[i]}")
        
        kpaths.append(start_k + end_k)
        i += 1

    return np.array(kpaths)

kpaths = read_kpath("KPATH.in")
#kpaths = np.array([
#    [0.0000000000, 0.0000000000, 0.0000000000, 0.5000000000, 0.5000000000, 0.5000000000],
#    [0.5000000000, 0.5000000000, 0.5000000000, 0.8113023911, 0.1886976089, 0.5000000000],
#    [0.5000000000, -0.1886976089, 0.1886976089, 0.5000000000, 0.0000000000, 0.0000000000],
#    [0.5000000000, 0.0000000000, 0.0000000000, 0.0000000000, 0.0000000000, 0.0000000000],
#    [0.0000000000, 0.0000000000, 0.0000000000, 0.3443488044, -0.3443488044, 0.0000000000],
#    [0.6556511956, 0.0000000000, 0.3443488044, 0.5000000000, 0.0000000000, 0.5000000000],
#    [0.5000000000, 0.0000000000, 0.5000000000, 0.0000000000, 0.0000000000, 0.0000000000],
#])

Total_N_grids = 200
if len(sys.argv) > 1:
    Total_N_grids = int(sys.argv[1])
else:
    Total_N_grids = 200

print("Total k-points on the k-path = ", Total_N_grids," (default=200)\n")


def kpath_print(lattice_vec, kpaths, Total_N_grids):
    print("Starting kpoints generation for the band path...")

    Ra, Rb, Rc = lattice_vec
    volume = np.dot(Ra, np.cross(Rb, Rc))
    reciprocal_vec = [
        2 * np.pi * np.cross(Rb, Rc) / volume,
        2 * np.pi * np.cross(Rc, Ra) / volume,
        2 * np.pi * np.cross(Ra, Rb) / volume,
    ]

    kpath_list = []
    pathlength_list = []

    for klist in kpaths:
        pathdiff = klist[3:7] - klist[0:3]
        diff_cart = sum([pathdiff[i] * reciprocal_vec[i] for i in range(3)])
        pathlength = np.linalg.norm(diff_cart)
        pathlength_list.append(pathlength)

    length_total = sum(pathlength_list)
    kn_list = np.round(np.array(pathlength_list) / (length_total / Total_N_grids)).astype(int)

    print("\npathlength_list\n", pathlength_list)
    print(np.cumsum(pathlength_list))
    print("length_total:", length_total)
    print("\nkn_list", np.sum(kn_list), "\n", kn_list)
    #1 Explicit k-path list
    #2 199
    #3 Fractional
    F = open("KPOINTS", "w")
    F.write("Explicit k-path list\n")
    F.write(str(np.sum(kn_list))+"\n")
    F.write("Fractional\n")
    for i, klist in enumerate(kpaths):
        kstart = klist[:3]
        kend = klist[3:]
        for kn in range(kn_list[i]):
            if kn_list[i] > 1:
                kpoint = kstart + (kend - kstart) * kn / (kn_list[i] - 1)
            else:
                kpoint = kstart
            kpath_list.append(kpoint)
            #print(f"{kpoint[0]:10f} {kpoint[1]:10f} {kpoint[2]:10f} 1")
            F.write(f"{kpoint[0]:10f} {kpoint[1]:10f} {kpoint[2]:10f} 1\n")
            
    F.close()
    print("The calculation has been normally finished.\n")

kpath_print(lattice_vec, kpaths, Total_N_grids)
