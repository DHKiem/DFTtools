import matplotlib.pyplot as plt
import numpy as np

data = np.loadtxt("TDOS")

plt.figure(figsize=(6,4))

if len(data[0,:]) < 4:
  plt.plot(data[:,0], data[:,1], color='brown', lw=1.0)
else:
  plt.plot(data[:,0], data[:,1], color='lightred', lw=1.0)
  plt.plot(data[:,0], data[:,2], color='royalblue', lw=1.0)


plt.xlim(-10, 10)
plt.xlabel("Energy (eV)", fontsize=13)
plt.ylabel("DOS (states/eV)", fontsize=13)
plt.xticks(fontsize=11)
plt.yticks(fontsize=11)

plt.tight_layout()
plt.show()

