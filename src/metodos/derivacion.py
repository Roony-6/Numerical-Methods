import numpy as np
import pandas as pd
from sympy import sympify, symbols, lambdify


class DerivacionNumerica:
    def __init__(self, x, y):
        self.x = np.asarray(x, dtype=float)
        self.y = np.asarray(y, dtype=float)

        if len(self.x) != len(self.y):
            raise ValueError("Los vectores x e y deben tener la misma cantidad de puntos.")
        if len(self.x) < 3:
            raise ValueError("Se requieren al menos 3 puntos para aproximar la derivada.")

        espaciados = np.diff(self.x)
        if np.isclose(espaciados[0], 0) or not np.allclose(espaciados, espaciados[0]):
            raise ValueError("Los puntos x deben estar uniformemente espaciados y ser distintos.")

        self.h = espaciados[0]
        self.f = None

    @classmethod
    def desde_funcion(cls, funcion_str, a, b, n):
        if n < 2:
            raise ValueError("Se requieren al menos n = 2 subintervalos.")
        x_sym = symbols('x')
        f = lambdify(x_sym, sympify(funcion_str), modules="numpy")
        x = np.linspace(a, b, n + 1)
        y = np.array([f(valor) for valor in x], dtype=float)
        instancia = cls(x, y)
        instancia.f = f
        return instancia

    def calcular_derivadas(self):
        n_pts = len(self.x)
        resultados = []

        for i in range(n_pts):
            derivada, formula = self._mejor_formula(i, n_pts)
            resultados.append({
                "x": self.x[i],
                "f(x)": self.y[i],
                "f'(x)": derivada,
                "Fórmula Usada": formula,
            })

        return pd.DataFrame(resultados)

    def _mejor_formula(self, i, n_pts):
        """Selecciona la fórmula más precisa disponible para el punto i:
        primero 5 puntos (O(h^4)), luego 3 puntos (O(h^2))."""
        y, h = self.y, self.h

        if 2 <= i <= n_pts - 3:
            derivada = (y[i - 2] - 8 * y[i - 1] + 8 * y[i + 1] - y[i + 2]) / (12 * h)
            return derivada, "5 Puntos Central"

        if i + 4 <= n_pts - 1:
            derivada = (-25 * y[i] + 48 * y[i + 1] - 36 * y[i + 2]
                        + 16 * y[i + 3] - 3 * y[i + 4]) / (12 * h)
            return derivada, "5 Puntos Progresiva"

        if i - 4 >= 0:
            derivada = (25 * y[i] - 48 * y[i - 1] + 36 * y[i - 2]
                        - 16 * y[i - 3] + 3 * y[i - 4]) / (12 * h)
            return derivada, "5 Puntos Regresiva"

        if 1 <= i <= n_pts - 2:
            derivada = (y[i + 1] - y[i - 1]) / (2 * h)
            return derivada, "3 Puntos Central"

        if i == 0:
            derivada = (-3 * y[0] + 4 * y[1] - y[2]) / (2 * h)
            return derivada, "3 Puntos Progresiva"

        derivada = (y[i - 2] - 4 * y[i - 1] + 3 * y[i]) / (2 * h)
        return derivada, "3 Puntos Regresiva"

    @staticmethod
    def richardson(f, x, h_inicial, tol=1e-6, max_iter=20):
        """
        Calcula la derivada usando extrapolación de Richardson.

        Args:
            f: función a derivar
            x: punto donde calcular la derivada
            h_inicial: paso inicial para diferencias finitas
            tol: tolerancia de error para convergencia
            max_iter: máximo número de iteraciones

        Returns:
            (derivada_aproximada, tabla_richardson, historial, convergió)
        """
        historial = []

        def diferencia_central(x, h):
            return (f(x + h) - f(x - h)) / (2 * h)

        # Inicializar tabla de Richardson
        tabla_richardson = []

        for i in range(max_iter):
            h = h_inicial / (2 ** i)
            # Primera columna: diferencias centrales
            d0 = diferencia_central(x, h)
            tabla_richardson.append([d0])

            # Extrapolación de Richardson
            for j in range(1, i + 1):
                h_ratio = 2 ** (2 * j)
                d_mejorada = (h_ratio * tabla_richardson[i][j - 1] -
                             tabla_richardson[i - 1][j - 1]) / (h_ratio - 1)
                tabla_richardson[i].append(d_mejorada)

            # Verificar convergencia (usando elemento diagonal)
            if i > 0:
                error = abs(tabla_richardson[i][i] - tabla_richardson[i - 1][i - 1])
                historial.append({
                    'iteracion': i,
                    'aproximacion': tabla_richardson[i][i],
                    'h': h,
                    'error': error
                })

                if error < tol:
                    derivada_final = tabla_richardson[i][i]
                    convergio = True
                    return derivada_final, tabla_richardson, historial, convergio

        derivada_final = tabla_richardson[max_iter - 1][max_iter - 1]
        convergio = False
        return derivada_final, tabla_richardson, historial, convergio
