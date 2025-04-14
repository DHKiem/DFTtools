## Apr 2025
## D.H. Kiem
## ../ : scf directory
## ./ : band directory
## ../dos/ : dos directory
## after non-self consistent calculation, 
## vaspkit 211 at band
## vaspkit 111 at dos

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Agg')
from matplotlib.gridspec import GridSpec
import re

bandfile = "BAND.dat"
dosfile  = "../dos/TDOS.dat"

linecolor = "forestgreen"

y_range = [-8,10]
dos_range = [0, 70]

outputfigure = "banddos.png"

############ Figure config ############
data1 = np.loadtxt(bandfile)
data2 = np.loadtxt(dosfile)

fig  = plt.figure(figsize=(8,6))
gs = GridSpec(1, 2, width_ratios=[2, 1])
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

ax1.set_ylim(y_range)
ax2.set_ylim(y_range)
ax2.set_yticks(y_range,[" ", " "])

klabel_info = []


with open("KLABELS", "r") as f:
    for line in f:
        words = line.strip().split()
        if len(words) == 2:
            klabel_info.append(line.strip())
            
band_range = [float(klabel_info[0].split()[1]), float(klabel_info[-1].split()[1])] 
k_label       = [ktemp.split()[0] for ktemp in klabel_info]
k_label_coord = [float(ktemp.split()[1]) for ktemp in klabel_info]
print("klabel_info: ", klabel_info)
print("Band range: ", band_range)
print("k_label: ", k_label)
print("k_label: ", k_label_coord)
ax1.set_xlim(band_range)
ax2.set_xlim(dos_range)

ax1.set_xticks( k_label_coord ,  k_label)

ax1.set_ylabel('Energy (eV)', fontsize = 14)
ax2.set_xlabel('DOS (states/eV)', fontsize = 12)


pattern = re.compile(r"alpha\+bet\s*:\s*([-+]?\d*\.\d+|\d+)")
Efermi_band = None
Efermi_scf  = None
with open("OUTCAR", "r") as f:
    for line in f:
        match = pattern.search(line)
        if match:
            Efermi_band = float(match.group(1))
with open("../OUTCAR", "r") as f:
    for line in f:
        match = pattern.search(line)
        if match:
            Efermi_scf  = float(match.group(1))

correction_fermi =  Efermi_band - Efermi_scf 

ax1.plot(data1[:,0], data1[:,1]- correction_fermi, color=linecolor)
ax2.plot(data2[:,1], data2[:,0], color=linecolor)

plt.tight_layout()
plt.savefig(outputfigure)
print("Output: ", outputfigure)
#plt.show()

