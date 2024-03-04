#!/usr/bin/env python 
##########################
# This code is written for projected (fat) band plot in OpenMX
# Developer : Do Hoon Kiem
# Last update : 2023-04-01
version = "v0.1.1"
##########################

import numpy as np
import matplotlib.pyplot as plt

####### File inputs ######
datafile_up = "../TARGETFILE.unfold_orbup"
datafile_dn = "../TARGETFILE.unfold_orbdn"
print(" up band file : ", datafile_up)
print(" dn band file : ", datafile_dn)

data_up = np.loadtxt(datafile_up)
data_dn = np.loadtxt(datafile_dn)
######## File inputs ######

######## Figure settings ######
colorscheme=[ '#C2185B' , '#42A5F5' ]          
######## Figure settings ######

############ parameter settings ############
atomic_info = np.array( [[18, 26], [54, 13], [50, 13]]) # set of  [number of atoms, number of orbitals for each atom] # automatic checking will be updated
atomic_group = [
                [list(range(1,   1+6)) + list(range(19,19+18))] , #layer 1
                [list(range(7,   7+6)) + list(range(37,37+18))] , #layer 2
                [list(range(13, 13+6)) + list(range(55,55+18))] , #layer 3
                [list(range(73,73+50))  ]  #graphene
                                        ]
group_names = [ 'CrI3_layer1', 'CrI3_layer2', 'CrI3_layer3', 'Graphene']
############ parameter settings ############




Num_atom = sum([atomic_info[i][0] for i in range(len(atomic_info))])
print("Total number of atom: ", Num_atom)
orbital_for_atom = []

for atomic in atomic_info:
  for i in range(atomic[0]):
    orbital_for_atom += [atomic[1]]
print(len(orbital_for_atom), orbital_for_atom)

orbital_group = [[False for j in range(sum(orbital_for_atom)+2 )] for i in atomic_group]
#print(orbital_group)

for (group_index, atomic) in enumerate(atomic_group):
  print(atomic[0])
  for atom in atomic[0]:
    print(atom, end = ' ')
    print(sum(orbital_for_atom[0:atom-1]))
    for j in list(range(sum(orbital_for_atom[0:atom-1]) + 2 , sum(orbital_for_atom[0:atom])+2 ) ):
      orbital_group[group_index][j] = True


for (i,orbindex) in enumerate(orbital_group):
  ######## Figure settings ######
  fig = plt.figure(figsize=(4,3.4))

  plt.ylabel("Energy (eV)",fontsize=13)
  plt.xticks([0.0, 0.156612, 0.247023, 0.427845], ["Γ", "M", "K", "Γ"], fontsize=12)
  
  plt.xlim(0.0,0.427845)
  plt.ylim(-1.0,1.0)
  
  plt.yticks([-1.0, 0.0, 1.0], fontsize=12)
  plt.axhline(0.0, linewidth=0.4, color='gray')
  plt.tight_layout()
  ######## Figure settings ######
  #print(orbindex)
  #print(len(orbindex))

  upcirclesize = np.sum( data_up[:,orbindex] , axis = 1)
  upmaxintensity = np.max(upcirclesize)
  dncirclesize = np.sum( data_dn[:,orbindex] , axis = 1)
  dnmaxintensity = np.max(dncirclesize)
  plt.scatter(data_up[:,0],data_up[:,1], s=upcirclesize*10.5, color=colorscheme[0], alpha=upcirclesize/upmaxintensity *0.7)
  plt.scatter(data_dn[:,0],data_dn[:,1], s=dncirclesize*10.5, color=colorscheme[1], alpha=dncirclesize/dnmaxintensity *0.7)
  plt.show()
  plt.savefig(group_names[i]+".pdf")
