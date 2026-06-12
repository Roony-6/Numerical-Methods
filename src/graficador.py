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

    def graficar_derivada(self, df_resultados):
        titulo = self.ax.get_title()
        plt.close(self.fig)
        self.fig, (ax_f, ax_df) = plt.subplots(2, 1, figsize=(9, 7), sharex=True)
        self.ax = ax_f

        x = df_resultados["x"]

        ax_f.plot(x, df_resultados["f(x)"], color='tab:blue', marker='o',
                  markersize=4, linewidth=2, label="f(x)")
        ax_f.set_title(titulo)
        ax_f.set_ylabel("f(x)")
        ax_f.grid(True, linestyle='--', alpha=0.7)
        ax_f.axhline(0, color='black', linewidth=1.5, alpha=0.5)
        ax_f.legend()

        ax_df.plot(x, df_resultados["f'(x)"], color='tab:red', marker='s',
                   markersize=4, linewidth=2, label="f'(x) aproximada")
        ax_df.set_xlabel("x")
        ax_df.set_ylabel("f'(x)")
        ax_df.grid(True, linestyle='--', alpha=0.7)
        ax_df.axhline(0, color='black', linewidth=1.5, alpha=0.5)
        ax_df.legend()

        self.fig.tight_layout()
        return self.fig

    def graficar_area_bajo_curva(self, f, a, b, puntos_x=None):
        margen = (b - a) * 0.15 or 1.0
        x = np.linspace(a - margen, b + margen, 400)
        y = [f(val) for val in x]
        self.ax.plot(x, y, label="f(x)", linewidth=2, color='tab:blue')

        x_area = np.linspace(a, b, 400)
        y_area = [f(val) for val in x_area]
        self.ax.fill_between(x_area, y_area, alpha=0.35, color='tab:orange',
                             label="Área aproximada")

        if puntos_x is not None:
            for px in puntos_x:
                self.ax.vlines(px, 0, f(px), color='tab:red', linestyle='--',
                               alpha=0.8, linewidth=1)

        self.ax.legend()
        return self.fig

    def graficar_edo(self, df_resultados, titulo="Aproximación de EDO"):
        self.ax.set_title(titulo)
        self.ax.set_ylabel("y(x)")
        self.ax.plot(df_resultados["x"], df_resultados["y_aprox"],
                     color='tab:blue', marker='o', markersize=4,
                     linewidth=2, label="y aproximada")
        self.ax.legend()
        return self.fig

    def graficar_sistema_edo(self, df_resultados, titulo="Sistema de EDO"):
        self.ax.set_title(titulo)
        self.ax.set_ylabel("y(x)")
        columnas_y = [c for c in df_resultados.columns
                      if c.startswith('y') and c != 'y_aprox']
        for columna in columnas_y:
            self.ax.plot(df_resultados["x"], df_resultados[columna],
                         marker='o', markersize=4, linewidth=2,
                         label=f"{columna}(x)")
        self.ax.legend()
        return self.fig

    def dibujar_frame_bungee(self, y_pos, L, max_y):
        # Se limpia el eje en lugar de crear una figura nueva por frame
        self.ax.clear()
        color_cuerda = 'red' if y_pos > L else 'gray'
        self.ax.plot([0, 0], [0, -y_pos], color=color_cuerda, linewidth=2.5,
                     label="Cuerda estirada" if y_pos > L else "Cuerda")
        self.ax.plot(0, -y_pos, 'o', color='tab:blue', markersize=14,
                     label="Saltador")
        self.ax.axhline(-L, color='black', linestyle='--', linewidth=1,
                        alpha=0.5, label="Longitud natural (L)")
        self.ax.axhline(0, color='saddlebrown', linewidth=4)

        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-max_y, 10)
        self.ax.set_xticks([])
        self.ax.set_ylabel("Posición (m)")
        self.ax.set_title("Simulación de Salto Bungee")
        self.ax.legend(loc='lower right', fontsize=8)
        return self.fig

    def obtener_figura(self):
        return self.fig