import numpy as np
import matplotlib.pyplot as plt

####### File inputs ######
bandfile = "../CrI3.Band"
print("band file : ", bandfile)

F = open(bandfile,'r')
L = F.readlines()
F.close()
######## File inputs ######







######### Figure settings ######
colorscheme=[ '#C2185B' , '#42A5F5' ]
fig = plt.figure(figsize=(4,3.4))

plt.ylabel("Energy (eV)",fontsize=13)
plt.xticks([0.0, 0.156612, 0.247023, 0.427845], ["Γ", "M", "K", "Γ"], fontsize=12)

plt.xlim(0.0,0.427845)
plt.ylim(-2.0,2.0)
linewidth = 0.5

plt.yticks([-2.0,-1.0, 0.0, 1.0, 2.0], fontsize=12)
plt.axhline(0.0, linewidth=0.4, color='gray',linestyle='--')
plt.tight_layout()
######### Figure settings ######












print("Total lines of band file: ", len(L))
NBANDS = int(L[0].split()[0])
spintype = int(L[0].split()[1] )
Nkpath = int(L[2].split()[0])
Efermi = float(L[0].split()[2])
Gv = np.array([np.array(L[1].split()[0:3], dtype = 'float'), np.array(L[1].split()[3:6], dtype = 'float'), np.array(L[1].split()[6:9], dtype = 'float') ])

print("Number of bands: ", NBANDS)
print("Spin type: ", spintype)
print("Number of k-path : ", Nkpath)
print("Fermi energy : ", Efermi)
print("Reciprocal lattice vector: ", Gv)
kpath = [[] for i in range(Nkpath)]
Nkpoints = 0 
for i in range(Nkpath):
  #print(L[3+i],end = '')
  kpath[i] = [int(L[3+i].split()[0]),  
          [float(L[3+i].split()[1]), float(L[3+i].split()[2]), float(L[3+i].split()[3])], 
          [float(L[3+i].split()[4]), float(L[3+i].split()[5]), float(L[3+i].split()[6])], 
          [L[3+i].split()[7], L[3+i].split()[8]]
          ] 
  Nkpoints += kpath[i][0]
print("k-path: ", kpath)
print("Total k points: ", Nkpoints)

#file check
if (len(L) != 3 + Nkpath + Nkpoints * (spintype+1) * 2):
  print("Check your inputfile")
  exit()


bands = [np.zeros((Nkpoints, NBANDS+1)) for i in range(spintype+1)]

kposition = np.zeros((Nkpoints+1,3)) 
kx = 0.0

for i in range(Nkpoints):
  refline = 3 + Nkpath + i * (spintype+1) * 2
  #print(refline)
  kposition[i+1,:] = Gv[0]* float(L[refline].split()[1]) + Gv[1]* float(L[refline].split()[2]) + Gv[2]* float(L[refline].split()[3]) 
  kdistance = kposition[i+1,:] - kposition[i,:]
  klength = np.linalg.norm(kdistance)
  kx += klength
  for j in range(spintype+1):
    bands[j][i,0] = kx
    bands[j][i,1:] = np.array(L[refline+1+2*j].split()) 


for j in range(spintype+1):
  for i in range(NBANDS):
    plt.plot(bands[j][:,0], (bands[j][:,i]-Efermi)*27.2113845 ,color=colorscheme[j], linewidth=linewidth, alpha = 0.7)
#plt.savefig("TotalBand.pdf")
plt.show()


