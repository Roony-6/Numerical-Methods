import numpy as np
import pandas as pd


class SimuladorBungee:
    G = 9.81

    def calcular_trayectoria(self, m, k, c, L, t_final, dt):
        n = int(round(t_final / dt))
        t = np.linspace(0, n * dt, n + 1)
        y = np.zeros(n + 1)
        v = np.zeros(n + 1)

        def derivadas(yi, vi):
            dv = self.G - (c / m) * vi - (k / m) * max(0.0, yi - L)
            return vi, dv

        for i in range(n):
            k1_y, k1_v = derivadas(y[i], v[i])
            k2_y, k2_v = derivadas(y[i] + dt * k1_y / 2, v[i] + dt * k1_v / 2)
            k3_y, k3_v = derivadas(y[i] + dt * k2_y / 2, v[i] + dt * k2_v / 2)
            k4_y, k4_v = derivadas(y[i] + dt * k3_y, v[i] + dt * k3_v)
            y[i + 1] = y[i] + (dt / 6) * (k1_y + 2 * k2_y + 2 * k3_y + k4_y)
            v[i + 1] = v[i] + (dt / 6) * (k1_v + 2 * k2_v + 2 * k3_v + k4_v)

        return pd.DataFrame({'t': t, 'y': y})
