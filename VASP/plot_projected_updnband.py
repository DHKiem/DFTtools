## Jul 2025
## D.H. Kiem
## ../ : scf directory
## ./ : band directory
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
    ["Fe", ["d"], "orangered"],
    ["Te", ["p"], "forestgreen"],
]
NumEle = len(atom_orbital_list)

E_range = [-10,10]
dos_range = [0, 60]

############ Figure config ############
fig  = plt.figure(figsize=(10,6))
gs = GridSpec(1, 2, width_ratios=[1, 1])
ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1])

ax1.set_ylim(E_range)
ax2.set_ylim(E_range)
ax2.set_yticks(E_range,[" ", " "])

ax1.set_ylabel('Energy (eV)', fontsize = 14)


############ Figure config ############
pattern = re.compile(r"E\-fermi\s*:\s*([-+]?\d*\.\d+|\d+)")
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

print("Fermi Energy: ",Efermi_scf)
correction_fermi =  Efermi_scf - Efermi_band

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
ax2.set_xlim(band_range)
ax1.set_xticks( k_label_coord ,  k_label)
ax2.set_xticks( k_label_coord ,  k_label)



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
maxbandvalueup = 0.0 #np.max(total_band)
maxbandvaluedn = 0.0 #np.max(total_band)



file1 = "BAND.dat"
#linecolor = "black"
data1 = np.loadtxt(file1)
ax1.plot(data1[:,0], data1[:,1]- correction_fermi, color='gray', linewidth = 0.1)
ax2.plot(data1[:,0], data1[:,2]- correction_fermi, color='gray', linewidth = 0.1)


####### File load #######
#for (element,orbital,linecolor) in zip(filenamelist,orbitallist, colors):
for [element,orbital,linecolor] in atom_orbital_list: 
  pbandupfile = "PBAND_"+element+"_UP.dat"
  pbanddnfile = "PBAND_"+element+"_DW.dat"
  #pdosfile = "../dos/PDOS_"+element+".dat"

  pbandup = np.loadtxt(pbandupfile)
  pbanddn = np.loadtxt(pbanddnfile)
  

  orbital_index = orbital_indexing(orbital)
  orbital_index = orbital_index.astype(int)
  print(element, orbital, orbital_index)
  print(type(orbital_index[0]))
  total_bandup = np.zeros_like(pbandup[:, 2])
  total_banddn = np.zeros_like(pbanddn[:, 2])
  
  for i in orbital_index:
    print(i)
    total_bandup += pbandup[:,i+1]
    total_banddn += pbanddn[:,i+1]
    #total_dos += pdos[:,i]

  if np.max(total_bandup) > maxbandvalueup:
    maxbandvalueup = np.max(total_bandup)
  if np.max(total_banddn) > maxbandvaluedn:
    maxbandvaluedn = np.max(total_banddn)


outputfilename = ""

for [element,orbital,linecolor] in atom_orbital_list: 
  pbandupfile = "PBAND_"+element+"_UP.dat"
  pbanddnfile = "PBAND_"+element+"_DW.dat"
  
  outputfilename += element+"_"+''.join(orbital)+"_"

  pbandup = np.loadtxt(pbandupfile)
  pbanddn = np.loadtxt(pbanddnfile)
  

  orbital_index = orbital_indexing(orbital)
  orbital_index = orbital_index.astype(int)

  total_bandup = np.zeros_like(pbandup[:, 2])
  total_banddn = np.zeros_like(pbanddn[:, 2])
  
  for i in orbital_index:
    
    total_bandup += pbandup[:,i+1]
    total_banddn += pbanddn[:,i+1]
    

  ax1.scatter(pbandup[:,0], pbandup[:,1]-correction_fermi, s=total_bandup*1.2, color=linecolor, alpha = total_bandup/maxbandvalueup*1.0 )
  ax2.scatter(pbanddn[:,0], pbanddn[:,1]-correction_fermi, s=total_banddn*1.2, color=linecolor, alpha = total_banddn/maxbandvaluedn*1.0 ,label=element+"_"+''.join(orbital))

  

ax2.legend()




plt.tight_layout()
plt.savefig(outputfilename+"_updnband.png")

print("Output: ", outputfilename+"_updnband.png")

#plt.show()

