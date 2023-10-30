import numpy as np
import sys

target_files = [sys.argv[1], sys.argv[2]]
outfile = sys.argv[3]


F = open(outfile, "w")
for targetfile in target_files:
  print("input file: ", targetfile)
  if 'fermi_proj' not in locals():
    F0 = open(targetfile, "r")
    L = F0.readlines()
    F0.close()
    kn = L[0].split()
    bandn = int(L[2].split()[0])
    for i in range(6 + int(kn[0]) * int(kn[1]) * int(kn[2])* bandn):
      F.write(L[i])
    data = np.loadtxt(targetfile, skiprows = 6 + int(kn[0]) * int(kn[1]) * int(kn[2])* bandn )
    fermi_proj = data
  else:
    data = np.loadtxt(targetfile, skiprows = 6 + int(kn[0]) * int(kn[1]) * int(kn[2])* bandn )
    fermi_proj *= data

for fermivalue in fermi_proj:
  F.write(str(fermivalue)+"\n")
F.close()
print("output_name: ", outfile)
print("max: ", np.max(fermi_proj))
print("min: ", np.min(fermi_proj))
print("average: ", np.average(fermi_proj))


    
