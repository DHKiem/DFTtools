#!/usr/bin/env python 
##########################
# This code is written for doscar analysis for VASP
# Developer : Do Hoon Kiem
# initiated : 2019. Jan. 17th
# Last update : 2023-09-12
version = "v0.1.2"
##########################

## DOSCAR -> TDOS | PDOS 
# mode 1 : TDOS
# mode 2 : PDOS
# mode 3 : all 

import os,sys

def totaldos(inputfile):
  F = open(inputfile)
  L = F.read().split("\n")[:-1]
  F.close()
  Efermi = float(L[5].split()[3]) # Fermi energy from DOSCAR
  print("Fermi energy = ",Efermi)
  
  AN = int(L[0].split()[0])  # Total Number of Atom
  GN = int(L[5].split()[2])  # Total Number of Grid
  print("Number of atoms = ",AN)
  print("Number of grids = ",GN)
  
  L = L[6:]
  spintype = len(L[0].split()) # 3 for unpol or noncol and 5 for pol
  #print("spin type ",spintype)
  ####### writing TDOS #######
  print("Generating 'TDOS' file...")
  F = open("TDOS", "w")
  for i in range(0, GN) :
    Eshifted = float(L[i].split()[0])-Efermi
    if spintype > 4:
      F.write("%f %s %s %s %s\n"%(Eshifted,L[i].split()[1],L[i].split()[2],L[i].split()[3],L[i].split()[4]))
    else:
      F.write("%f %s %s\n"%(Eshifted,L[i].split()[1],L[i].split()[2])) 
  F.close()
  print("TDOS generated.")
  ############################

######## writing PDOS files ##############
def pdos(inputfile):
  F = open(inputfile)
  L = F.read().split("\n")[:-1]
  F.close()
  Efermi = float(L[5].split()[3]) # Fermi energy from DOSCAR
  print("Fermi energy = ",Efermi)

  AN = int(L[0].split()[0])  # Total Number of Atom
  GN = int(L[5].split()[2])  # Total Number of Grid
  print("Number of atoms = ",AN)
  print("Number of grids = ",GN)
  L = L[6:]
  spintype = len(L[0].split())

  TDOS2   = [[0 for j in range((spintype>4)+1)] for i in range(GN)]
  Eenergy = [ 0 for i in range(GN)]

  print("Generating 'PDOS_N' files...")
  for an in range(1, AN+1) :
      F = open("PDOS_%d" % an, "w")
      num_orb = len(L[1*(GN+1)+1].split())
      
      for l in range(0, GN) :
          lp = an*(GN+1) +l
          Eshifted=float(L[lp].split()[0])-Efermi
          F.write("%f %s\n"%(Eshifted, ' '.join(L[lp].split()[1:])) )
          #F.write("%f %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s %s\n"%(Eshifted,L[lp].split()[1],L[lp].split()[2],L[lp].split()[3],L[lp].split()[4],L[lp].split()[5],L[lp].split()[6],L[lp].split()[7],L[lp].split()[8],L[lp].split()[9],L[lp].split()[10],L[lp].split()[11],L[lp].split()[12],L[lp].split()[13],L[lp].split()[14],L[lp].split()[15],L[lp].split()[16],L[lp].split()[17],L[lp].split()[18]))
          Eenergy[l-1]=Eshifted

          for j in range(1, num_orb, 1):###################### 2019. Feb. 29th
            if spintype < 4:
              TDOS2[l-1][0] += float(L[lp].split()[j])
            else:
              if j%2 == 1:
                TDOS2[l-1][0] += float(L[lp].split()[j])
              else:
                TDOS2[l-1][1] += float(L[lp].split()[j])
      F.close()
  print("PDOS_N generated.")
  ####### TDOS from PDOS ##################
  F3 = open("TDOS2","w")
  for i in range(GN):
    F3.write("%f "%(Eenergy[i]))
    for dosspin in TDOS2[i]:
      F3.write("%f "%(dosspin))
    F3.write("\n")
    
  F3.close()    
##########################################


########## START MAIN ############
print("Hello! Thanks for using this DOSCAR analysis code.")
print("VERSION:",version)
print("How to use: 'python THISCODE doscar.vasp[default=DOSCAR] calmode[1|2|3 ; default=3]'\n")

inputfile = 'DOSCAR'
if len(sys.argv) > 1:
    inputfile = sys.argv[1]
else:
    inputfile = 'DOSCAR'

print("Your input file= ", inputfile,"\n")

filecheck = os.path.isfile(inputfile)
calmode = 3 
if filecheck:
  if len(sys.argv) > 2:
    calmode = sys.argv[2]
  else:
    calmode = input("What do you want to calculation? (1: TDOS, 2: PDOS, 3: all[default])\n=> ")
  if calmode == '1':
    totaldos(inputfile)
  elif calmode == '2':
    pdos(inputfile)
  else:
    totaldos(inputfile)
    pdos(inputfile)
else:
  print("No input structure file. Check your input. The default input is 'DOSCAR'")
  exit()

