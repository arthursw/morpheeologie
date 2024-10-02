#%%
import math
import numpy as np

rho = 950 # kg/mˆ3 masse volumique de la goutte
g = 9.80665 # m/sˆ2
rho0 = 900 # kg/mˆ3 masse volumique du milieu
rho_p = (rho0 - rho) / rho
gr = g * rho_p
eta = 0.1 # Viscosité dynamique du bassin
r = np.logspace(-2, 1, num=100) / 1000 # 0.01 # rayon de la goutte, mm
V0 = 0 # vitesse initiale

tau = 2 * rho * r * r / (9 * eta)

C = tau * (V0 - tau * gr)
z_tau = tau * tau * gr + C * ( 1 - 1 / math.exp(1) )

import matplotlib.pyplot as plt

plt.plot(r, z_tau * 1000)
plt.show()