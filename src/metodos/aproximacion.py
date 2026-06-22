import numpy as np
from sympy import symbols, expand, simplify, series, sympify

class Aproximador:
    """Clase para aproximación de funciones y ajuste de curvas."""

    @staticmethod
    def minimos_cuadrados(x, y, grado):
        """
        Ajuste polinomial por mínimos cuadrados.

        Args:
            x: array de valores x
            y: array de valores y
            grado: grado del polinomio de ajuste

        Returns:
            (polinomio_simbolico, coeficientes, error_cuadratico)
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        coeficientes = np.polyfit(x, y, grado)
        polinomio_numpy = np.poly1d(coeficientes)

        x_sym = symbols('x')
        polinomio_simbolico = 0
        for i, coef in enumerate(coeficientes):
            polinomio_simbolico += coef * (x_sym ** (grado - i))

        polinomio_simbolico = expand(polinomio_simbolico)

        y_ajuste = polinomio_numpy(x)
        error_cuadratico = np.sum((y - y_ajuste) ** 2)

        return polinomio_simbolico, coeficientes, error_cuadratico

    @staticmethod
    def polinomio_taylor(funcion_str, x0, grado):
        """
        Calcula el polinomio de Taylor.

        Args:
            funcion_str: expresión de la función como string
            x0: punto de expansión
            grado: grado del polinomio

        Returns:
            polinomio_simbolico simplificado
        """
        x = symbols('x')
        funcion = sympify(funcion_str)

        expansion = series(funcion, x, x0, n=grado + 1).removeO()
        polinomio_taylor = expand(expansion)

        return polinomio_taylor
