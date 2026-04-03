import matplotlib.pyplot as plt
import numpy as np

class Graficador:
    def __init__(self, titulo="Gráfica de Funciones"):
       
        plt.style.use('seaborn-v0_8-muted') 
        self.fig, self.ax = plt.subplots(figsize=(9, 6))
        self.ax.set_title(titulo)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("f(x)")
        self.ax.grid(True, linestyle='--', alpha=0.7)
        # Dibujamos el eje X (y=0) para ver la raíz claramente
        self.ax.axhline(0, color='black', linewidth=1.5, alpha=0.5)

    def graficar_funcion(self, f, a, b, label="f(x)"):
        x = np.linspace(a, b, 400)
        y = [f(val) for val in x]
        self.ax.plot(x, y, label=label, linewidth=2)
        self.ax.legend()

    def marcar_puntos(self, px, py, label="Iteraciones"):
        self.ax.scatter(px, py, color='red', s=40, zorder=5, label=label)
        self.ax.legend()

    def obtener_figura(self):
        return self.fig