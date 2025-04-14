## Apr 2025
## D.H. Kiem
## ../ : scf directory
## ./ : band directory
## ../dos/ : dos directory
## after non-self consistent calculation, 
## vaspkit 213 at band
## vaspkit 113 at dos

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import re

# data file
# rgb colors:  "orangered",  "royalblue", "brown", "navy", "purple","brown","black", "gray"
# orbital: s, p, d, t2g, eg
# format: [atom, orbital, color]

atom_orbital_list = [
    ["Ru", ["t2g"], "orangered"],
    ["Ru", ["eg"], "royalblue"],
]
NumEle = len(atom_orbital_list)

E_range = [-6,10]
dos_range = [0, 60]

############ Figure config ############
fig  = plt.figure(figsize=(8,6))
gs = GridSpec(1, 2, width_ratios=[2, 1])
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

ax1.set_ylim(E_range)
ax2.set_ylim(E_range)
ax2.set_yticks(E_range,[" ", " "])

ax1.set_ylabel('Energy (eV)', fontsize = 14)
ax2.set_xlabel('DOS (states/eV)', fontsize = 12)


############ Figure config ############
pattern = re.compile(r"alpha\+bet\s*:\s*([-+]?\d*\.\d+|\d+)")
Efermi_band = None
Efermi_scf  = None
with open("OUTCAR", "r") as f:
    for line in f:
        match = pattern.search(line)
        if match:
            Efermi_band = float(match.group(1))
with open("../dos/OUTCAR", "r") as f:
    for line in f:
        match = pattern.search(line)
        if match:
            Efermi_scf  = float(match.group(1))

print("Fermi Energy: ",Efermi_scf)
correction_fermi =  Efermi_band - Efermi_scf 

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



######
def orbital_indexing(atom_orbital):
  index = np.array([])
  for orbital in atom_orbital:
    print("orbital indexing", atom_orbital)
    if orbital == "s":
      index = np.append(index, np.array([1],dtype=int))
    elif orbital == "p":
      index = np.append(index, np.array([2,3,4], dtype=int))
    elif orbital == "d":
      index = np.append(index, np.array([5,6,7,8,9], dtype=int) )
    elif orbital == "t2g":
      index = np.append(index, np.array([5,6,8], dtype=int) )
    elif orbital == "eg":
      index = np.append(index, np.array([7,9], dtype=int) )
  return index

#####
maxbandvalue = 0.0 #np.max(total_band)



file1 = "BAND.dat"
#linecolor = "black"
data1 = np.loadtxt(file1)
ax1.plot(data1[:,0], data1[:,1]- correction_fermi, color='gray', linewidth = 0.1)


####### File load #######
#for (element,orbital,linecolor) in zip(filenamelist,orbitallist, colors):
for [element,orbital,linecolor] in atom_orbital_list: 
  pbandfile = "PBAND_"+element+".dat"
  pdosfile = "../dos/PDOS_"+element+".dat"

  pband = np.loadtxt(pbandfile)
  pdos  = np.loadtxt(pdosfile)

  orbital_index = orbital_indexing(orbital)
  orbital_index = orbital_index.astype(int)
  print(element, orbital, orbital_index)
  print(type(orbital_index[0]))
  total_band = np.zeros_like(pband[:, 2])
  total_dos = np.zeros_like(pdos[:, 2])
  for i in orbital_index:
    print(i)
    total_band += pband[:,i+1]
    total_dos += pdos[:,i]

  if np.max(total_band) > maxbandvalue:
    maxbandvalue = np.max(total_band)


outputfilename = ""

for [element,orbital,linecolor] in atom_orbital_list: 
  pbandfile = "PBAND_"+element+".dat"
  pdosfile = "../dos/PDOS_"+element+".dat"
  outputfilename += element+"_"+''.join(orbital)+"_"

  pband = np.loadtxt(pbandfile)
  pdos  = np.loadtxt(pdosfile)

  orbital_index = orbital_indexing(orbital)
  orbital_index = orbital_index.astype(int)
  #print(element, orbital, orbital_index)
  #print(type(orbital_index[0]))
  total_band = np.zeros_like(pband[:, 2])
  total_dos = np.zeros_like(pdos[:, 2])
  for i in orbital_index:
    #print(i)
    total_band += pband[:,i+1]
    total_dos += pdos[:,i]

  ax1.scatter(pband[:,0], pband[:,1]-correction_fermi, s=total_band*1.2, color=linecolor, alpha = total_band/maxbandvalue*1.0 )

  ax2.plot(total_dos, pdos[:,0], color=linecolor, label = element +"_"+ ''.join(orbital))


#outputfilename += ".png"

ax2.legend()




plt.tight_layout()
plt.savefig(outputfilename+".png")

print("Output: ", outputfilename+".png")

#plt.show()

