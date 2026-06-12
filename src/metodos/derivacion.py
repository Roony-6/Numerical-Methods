import numpy as np
from sympy import sympify, symbols, lambdify

class Derivacion:
    def __init__(self, function_str, a, b, n):
        x = symbols('x')
        expresion_simbolica = sympify(function_str)
        
        # Guardamos la función numérica
        self.f = lambdify(x, expresion_simbolica, modules="numpy")
        
        # n particiones generan n+1 puntos
        self.n = n
        self.x = np.linspace(a, b, n + 1)
        self.y = np.array(self.f(self.x))
        
        self.h = (b - a) / n
        
        # El vector de derivadas debe medir n+1 para cubrir todos los puntos
        self.y_prima = np.zeros(n + 1)

    def calcular_derivadas(self):
        """Aquí meterás el bucle para llenar self.y_prima usando las fórmulas"""
        historial = []
        
        for i in range(self.n + 1):
            # Lógica adaptativa según el índice 'i'
            if i == 0:
                # Extremo izquierdo: Progresiva de 3 puntos
                # Usamos self.y[0], self.y[1], self.y[2] y self.h
                self.y_prima[i] = (-3*self.y[0] + 4*self.y[1] - self.y[2]) / (2 * self.h)
                formula = "3 Puntos Progresiva"
            
            elif i == self.n:
                # Extremo derecho: Regresiva de 3 puntos
                self.y_prima[i] = (self.y[self.n - 2] - 4*self.y[self.n - 1] + 3*self.y[self.n]) / (2 * self.h)
                formula = "3 Puntos Regresiva"
            
            else:
                # Puntos intermedios: Central (La mejor aproximación estándar)
                self.y_prima[i] = (self.y[i + 1] - self.y[i - 1]) / (2 * self.h)
                formula = "Central"
                
            historial.append({
                "Punto": i,
                "x": self.x[i],
                "f(x)": self.y[i],
                "f'(x)": self.y_prima[i],
                "Fórmula": formula
            })
            
        return historial