import numpy as np
from sympy import symbols, simplify, expand

class Interpolador:
    def __init__(self, x, y):
        """
        Inicializa el interpolador con los datos.

        Args:
            x: array de valores x (list o np.array)
            y: array de valores y (list o np.array)
        """
        self.x = np.asarray(x, dtype=float)
        self.y = np.asarray(y, dtype=float)
        self.n = len(self.x)

        if len(self.y) != self.n:
            raise ValueError("x e y deben tener la misma longitud")

    def diferencias_divididas(self):
        """
        Calcula la tabla de diferencias divididas de Newton.

        Returns:
            (polinomio_simbolico, tabla_diferencias)
        """
        x = symbols('x')

        tabla = np.zeros((self.n, self.n))
        tabla[:, 0] = self.y

        for j in range(1, self.n):
            for i in range(self.n - j):
                tabla[i, j] = (tabla[i+1, j-1] - tabla[i, j-1]) / (self.x[i+j] - self.x[i])

        polinomio = tabla[0, 0]
        termino_actual = 1

        for j in range(1, self.n):
            termino_actual *= (x - self.x[j-1])
            polinomio += tabla[0, j] * termino_actual

        polinomio_simbolico = expand(polinomio)

        return polinomio_simbolico, tabla

    def lagrange(self):
        """
        Calcula el polinomio de interpolación de Lagrange.

        Returns:
            polinomio_simbolico simplificado
        """
        x = symbols('x')
        polinomio = 0

        for i in range(self.n):
            termino_lagrange = self.y[i]
            for j in range(self.n):
                if i != j:
                    termino_lagrange *= (x - self.x[j]) / (self.x[i] - self.x[j])
            polinomio += termino_lagrange

        return simplify(expand(polinomio))

    def neville(self, x_target):
        """
        Evalúa un punto usando el algoritmo de Neville.

        Args:
            x_target: valor x donde evaluar

        Returns:
            (valor_aproximado, matriz_q)
        """
        Q = np.zeros((self.n, self.n))
        Q[:, 0] = self.y

        for i in range(1, self.n):
            for j in range(1, i + 1):
                Q[i, j] = ((x_target - self.x[i-j]) * Q[i, j-1] -
                           (x_target - self.x[i]) * Q[i-1, j-1]) / (self.x[i] - self.x[i-j])

        valor_aproximado = Q[self.n - 1, self.n - 1]
        return valor_aproximado, Q
