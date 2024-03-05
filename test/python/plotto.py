import matplotlib.pyplot as plt
import numpy as np
T = np.arange(10)
E = np.arange(10)
SpcH = np.arange(10)
M = np.arange(10)
M_sus = np.arange(10)

plt.figure()
plt.plot(T, E, 'rx-')
plt.xlabel(r'Temperature $(\frac{J}{k_B})$')
plt.ylabel(r'$\langle E \rangle$ per site $(J)$')
plt.savefig("E8.pdf", format='pdf', bbox_inches='tight')

plt.figure()
plt.plot(T, SpcH, 'kx-')
plt.xlabel(r'Temperature $(\frac{J}{k_B})$')
plt.ylabel(r'$C_V$ per site $(\frac{J^2}{k_B^2})$')
plt.savefig("Cv8.pdf", format='pdf', bbox_inches='tight')

plt.figure()
plt.plot(T, M, 'bx-')
plt.xlabel(r'Temperature $(\frac{J}{k_B})$')
plt.ylabel(r'$\langle|M|\rangle$ per site $(\mu)$')
plt.savefig("M8.pdf", format='pdf', bbox_inches='tight')

plt.figure()
plt.plot(T, M_sus, 'gx-')
plt.xlabel(r'Temperature $(\frac{J}{k_B})$')
plt.ylabel(r'$\chi$ $(\frac{\mu}{k_B})$')
plt.savefig("chi8.pdf", format='pdf', bbox_inches='tight')

plt.tight_layout()
fig = plt.gcf()
plt.show()