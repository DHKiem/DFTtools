#!/usr/bin/env python 
##########################
# This code is written for analyzing NC-JX 
# Developer : Do Hoon Kiem
# Last update : 2024-01-09
version = "v0.1.1"
##########################

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

##### User inputs #####
system_name = "SYSTEMNAME"
atom1 = [1]   # target atom group1 
atom2 = [1,2,3,4]  # target atom group2

file_positions = ["to_x", "to_y", "to_z"] # clarify your Jx calculation directories with axes
csv_file_write = "off" # on | off for saving csv file
##### User inputs #####


# Create subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 4))

axs[0].axhline(linestyle='--')
for a1 in atom1:
  for a2 in atom2:
    print("\natom1, atom2: ",a1," ", a2)

    J_x = pd.read_csv(r"./"+file_positions[0]+"/jq.same.nc_allH_0.0/jq.same.nc_allH_"+system_name+"_atomij_"+str(a1)+"_"+str(a2)+"_[all_all]_ChemPdelta_0.0__NC.csv")
    J_y = pd.read_csv(r"./"+file_positions[1]+"/jq.same.nc_allH_0.0/jq.same.nc_allH_"+system_name+"_atomij_"+str(a1)+"_"+str(a2)+"_[all_all]_ChemPdelta_0.0__NC.csv")
    J_z = pd.read_csv(r"./"+file_positions[2]+"/jq.same.nc_allH_0.0/jq.same.nc_allH_"+system_name+"_atomij_"+str(a1)+"_"+str(a2)+"_[all_all]_ChemPdelta_0.0__NC.csv")
  
    Jxx = ( np.array(J_z.iloc[:,5]) + np.array(J_y.iloc[:,9]) )/2  
    Jyy = ( np.array(J_z.iloc[:,1]) + np.array(J_x.iloc[:,9]) )/2
    Jzz = ( np.array(J_x.iloc[:,5]) + np.array(J_y.iloc[:,1]) )/2

    J_Diag = (Jxx + Jyy + Jzz) /3
  
    Dx = ( np.array(J_x.iloc[:,6]) - np.array(J_x.iloc[:,8]) )/2 
    Dy = ( np.array(J_y.iloc[:,7]) - np.array(J_y.iloc[:,3]) )/2 
    Dz = ( np.array(J_z.iloc[:,2]) - np.array(J_z.iloc[:,4]) )/2 
    DM = np.sqrt(( Dx * Dx + Dy * Dy + Dz * Dz) )
  
    Gx = -( np.array(J_x.iloc[:,6]) + np.array(J_x.iloc[:,8]) )/2 
    Gy = -( np.array(J_y.iloc[:,7]) + np.array(J_y.iloc[:,3]) )/2 
    Gz = -( np.array(J_z.iloc[:,2]) + np.array(J_z.iloc[:,4]) )/2 

    Jxy = -J_z.iloc[:,4]
    Jyx = -J_z.iloc[:,2]
    Jyz = -J_x.iloc[:,8]
    Jzy = -J_x.iloc[:,6]
    Jzx = -J_y.iloc[:,3]
    Jxz = -J_y.iloc[:,7]

    df2 = pd.DataFrame({'Distance': J_z.iloc[:,0],
                        'Jxx': np.round(Jxx    ,  3),
                        'Jxy': np.round(Jxy    ,  3),
                        'Jxz': np.round(Jxz    ,  3),
                        'Jyx': np.round(Jyx    ,  3),
                        'Jyy': np.round(Jyy    ,  3),
                        'Jyz': np.round(Jyz    ,  3),
                        'Jzx': np.round(Jzx    ,  3),
                        'Jzy': np.round(Jzy    ,  3),
                        'Jzz': np.round(Jzz    ,  3),
                        'J_Diag': np.round(J_Diag, 3),
                        'Dx':  np.round(Dx   ,  3),
                        'Dy':  np.round(Dy   ,  3),
                        'Dz':  np.round(Dz   ,  3),
                        '|D|': np.round(DM   ,  3),
                        'Γx':  np.round(Gx   ,  3),
                        'Γy':  np.round(Gy   ,  3),
                        'Γz':  np.round(Gz   ,  3),
                        'rx': J_z.iloc[:,15],
                        'ry': J_z.iloc[:,16],
                        'rz': J_z.iloc[:,17],
                        'Rx': J_z.iloc[:,12],
                        'Ry': J_z.iloc[:,13],
                        'Rz': J_z.iloc[:,14]
                        })
    
    print(df2[df2.Distance <10])

    if csv_file_write == "on":
      df2.to_csv(system_name+"_"+str(a1)+"_"+str(a2)+".csv")


   # plot
    if not ('length' in locals()):
      length = df2.iloc[:,0]
      print(length)
      Js  = df2.iloc[:,10]
      DMs = df2.iloc[:,14]
    else:
      length = np.append(length, df2.iloc[:,0])
      Js  = np.append(Js,  df2.iloc[:,10])
      DMs = np.append(DMs, df2.iloc[:,14])
  length_sorted = np.sort(length)
  length_sorted_index = np.argsort(length)
  Js_sorted_by_length  = [Js[i] for i in length_sorted_index]
  DMs_sorted_by_length = [DMs[i] for i in length_sorted_index]

  axs[0].plot(length_sorted, Js_sorted_by_length,  label="atom"+str(a1), marker='o',  alpha=0.9, markersize=5)
  axs[1].plot(length_sorted, DMs_sorted_by_length, label="atom"+str(a1), marker='s',  alpha=0.9, markersize=5)
  del Js
  del length
  del DMs


axs[0].set_title('Heisenberg J')
axs[0].legend()
axs[0].set_xlabel("Distance (Å)")
axs[0].set_ylabel("J (meV)")

axs[1].set_title('DM interaction')
axs[1].legend()
axs[1].set_xlabel("Distance (Å)")
axs[1].set_ylabel("D (meV)")

# Overall plot title
plt.suptitle(system_name)

# Adjust layout
plt.tight_layout()

# Show the plot
plt.savefig("result_JD.png")
plt.show()


