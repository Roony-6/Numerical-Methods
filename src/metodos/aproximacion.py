import numpy as np
from sympy import symbols, expand, simplify, ln, exp, series, sympify

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
    def minimos_cuadrados_exponencial(x, y):
        """
        Ajuste exponencial: y = a * e^(bx)

        Args:
            x: array de valores x
            y: array de valores y

        Returns:
            (polinomio_simbolico, coeficientes, error_cuadratico)
            donde coeficientes = (a, b)
        """
        x = np.asarray(x, dtype=float)
        y = np.asarray(y, dtype=float)

        if np.any(y <= 0):
            raise ValueError("Para ajuste exponencial, todos los valores y deben ser positivos")

        ln_y = np.log(y)
        coeficientes_lineales = np.polyfit(x, ln_y, 1)
        b = coeficientes_lineales[0]
        ln_a = coeficientes_lineales[1]
        a = np.exp(ln_a)

        x_sym = symbols('x')
        polinomio_simbolico = a * exp(b * x_sym)
        polinomio_simbolico = simplify(polinomio_simbolico)

        y_ajuste = a * np.exp(b * x)
        error_cuadratico = np.sum((y - y_ajuste) ** 2)

        return polinomio_simbolico, (a, b), error_cuadratico

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
