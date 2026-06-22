import cmath

from sympy import sympify, symbols, lambdify, diff

class SolucionadorRaices:
    def __init__(self, function_str, tol=1e-6, max_iter=100):
        x = symbols('x')
        expresion_simbolica = sympify(function_str)
        
        derivada_simbolica = diff(expresion_simbolica,x)
        
        self.f = lambdify(x,expresion_simbolica, modules='numpy') 
        self.derivada_f = lambdify(x,derivada_simbolica, modules ='numpy')
        self.tol = tol
        self.max_iter = max_iter
        
        # Resultados despues de la ejecucion
        self.raiz = None
        self.convergio = False
        self.mensaje = ""
        
    def biseccion(self, a: float, b: float) -> tuple:
        historial = []
        fa = self.f(a)
        fb = self.f(b)

        # 1. Verificar si los extremos ya son raíces
        if fa == 0:
            self.convergio = True
            self.raiz = a
            self.mensaje = "El extremo 'a' es una raíz exacta."
            return self.raiz, historial
        if fb == 0:
            self.convergio = True
            self.raiz = b
            self.mensaje = "El extremo 'b' es una raíz exacta."
            return self.raiz, historial

        # 2. Verificar el Teorema del Valor Intermedio
        if fa * fb > 0:
            self.convergio = False
            self.mensaje = "No hay cambio de signo en el intervalo."
            return None, historial

        for i in range(self.max_iter):
            c_actual = (a + b) / 2
            fc = self.f(c_actual)

            # La cota de error en bisección es la mitad del intervalo
            cota_error = abs(b - a) / 2

            historial.append({
                "iteracion": i,
                "a": a,
                "b": b,
                "c": c_actual, 
                "f(c)": fc,
                "error": cota_error,
                "aprox": c_actual
            })

            # Verificación de raíz exacta o convergencia
            if abs(fc) < self.tol or (cota_error < self.tol):
                self.raiz = c_actual
                self.convergio = True
                self.mensaje = f"Convergencia lograda en iteración {i}."
                return self.raiz, historial

            # Actualización inteligente
            if fa * fc < 0:
                b = c_actual
                fb = fc
            else:
                a = c_actual
                fa = fc

        self.raiz = c_actual
        self.convergio = False
        self.mensaje = "Se alcanzó el máximo de iteraciones."
        return self.raiz, historial


    def secante(self, p0: float, p1: float) -> tuple:
        historial = []
        f0 = self.f(p0)
        f1 = self.f(p1) 

        for i in range(self.max_iter):
            if (f1 - f0) == 0:
                self.mensaje = "Error: División por cero (f(p1) - f(p0) = 0)."
                break

            p2 = p1 - (f1 * (p1 - p0)) / (f1 - f0)
            
            # Es un error absoluto entre iteraciones
            error_absoluto = abs(p2 - p1)

            historial.append({
                "iteracion": i,
                "p0": p0,
                "p1": p1,
                "aproximacion": p2,
                "error": error_absoluto,
                "aprox": p1
            })

            if error_absoluto < self.tol:
                self.raiz = p2
                self.convergio = True
                self.mensaje = f"Convergió en {i} iteraciones (error = {error_absoluto:.2e})."
                break
            
            # Actualización de parámetros
            p0 = p1
            f0 = f1 
            p1 = p2
            f1 = self.f(p1)

        else:
            self.raiz = p1
            self.convergio = False
            self.mensaje = "Se alcanzó el máximo de iteraciones sin converger."
            
        return self.raiz, historial
    
    def newton_rapshon(self, p0: float) -> tuple:
        historial = []
        
        for i in range(self.max_iter):
            derivada = self.derivada_f(p0)
            
            # Evitar división por cero
            if derivada == 0:
                self.convergio = False
                self.mensaje = "Error: La derivada es cero en este punto (división por cero)."
                return self.raiz, historial
                
            p1 = p0 - (self.f(p0) / derivada) 
            cota_error = abs(p1 - p0) 
            
            historial.append({
                "iteracion": i,
                "p0": p0,
                "p1": p1,
                "f(p1)": self.f(p1),
                "f'(p0)": derivada,
                "error": cota_error,
                "aprox": p1
            })  
            
            
            if self.f(p1) == 0 or cota_error <= self.tol:
                self.raiz = p1
                self.convergio = True
                self.mensaje = f"Convergió en {i+1} iteraciones con error {cota_error:.2e}"
                return self.raiz, historial
            
            
            p0 = p1


        self.raiz = p1
        self.convergio = False
        self.mensaje = "Se alcanzó el máximo de iteraciones sin converger."
            
        return self.raiz, historial


    def falsa_posicion(self, a: float, b: float) -> tuple:
        historial = []
        fa = self.f(a)
        fb = self.f(b)

        # 1. Verificar si los extremos ya son raíces
        if fa == 0:
            self.convergio = True
            self.raiz = a
            self.mensaje = "El extremo 'a' es una raíz exacta."
            return self.raiz, historial
        if fb == 0:
            self.convergio = True
            self.raiz = b
            self.mensaje = "El extremo 'b' es una raíz exacta."
            return self.raiz, historial

        # 2. Verificar el Teorema del Valor Intermedio
        if fa * fb > 0:
            self.convergio = False
            self.mensaje = "No hay cambio de signo en el intervalo."
            return None, historial

        c_prev = a

        for i in range(self.max_iter):
            # Evitar división por cero
            if (fa - fb) == 0:
                self.convergio = False
                self.mensaje = "Error: División por cero (f(a) - f(b) = 0)."
                return None, historial

            # Fórmula de la falsa posición
            c_actual = b - (fb * (a - b)) / (fa - fb)
            fc = self.f(c_actual)

            # Para la primera iteración, tomamos el tamaño del intervalo como error inicial
            error = abs(b - a) if i == 0 else abs(c_actual - c_prev)

            historial.append({
                "iteracion": i,
                "a": a,
                "b": b,
                "c": c_actual,
                "f(c)": fc,
                "error": error,
                "aprox": c_actual
            })

            # Verificación de raíz exacta o convergencia
            if abs(fc) < self.tol or (error < self.tol and abs(fc) < 0.01):
                self.raiz = c_actual
                self.convergio = True
                self.mensaje = f"Convergió en {i+1} iteraciones con error {error:.2e}."
                return self.raiz, historial

            # Actualización inteligente de los intervalos
            if fa * fc < 0:
                b = c_actual
                fb = fc
            else:
                a = c_actual
                fa = fc

            c_prev = c_actual

        self.raiz = c_actual
        self.convergio = False
        self.mensaje = "Se alcanzó el máximo de iteraciones sin converger."
        return self.raiz, historial
    
                
    def punto_fijo(self, g_str: str, p0: float) -> tuple:
        historial = []

        # g(x) es la función de iteración, independiente de f(x)
        x = symbols('x')
        g = lambdify(x, sympify(g_str), modules='numpy')

        for i in range(self.max_iter):
            p1 = g(p0)

            # El error es la diferencia absoluta entre iteraciones sucesivas
            cota_error = abs(p1 - p0)

            historial.append({
                "iteracion": i,
                "p0": p0,
                "p1": p1,
                "f(p1)": self.f(p1),
                "error": cota_error,
                "aprox": p1
            })

            # Condición de convergencia
            if cota_error < self.tol:
                self.raiz = p1
                self.convergio = True
                self.mensaje = f"Convergió en {i+1} iteraciones con error {cota_error:.2e}."
                return self.raiz, historial
            
            # Actualizamos p0 para la siguiente iteración
            p0 = p1

        self.raiz = p1
        self.convergio = False
        self.mensaje = "Se alcanzó el máximo de iteraciones (la función podría divergir)."

        return self.raiz, historial


    def muller(self, p0: float, p1: float, p2: float) -> tuple:
        historial = []
        f0 = self.f(p0)
        f1 = self.f(p1)
        f2 = self.f(p2)

        for i in range(self.max_iter):
            # Diferencias divididas para construir la parábola
            h0 = p1 - p0
            h1 = p2 - p1

            if h0 == 0 or h1 == 0 or (h1 + h0) == 0:
                self.convergio = False
                self.mensaje = "Error: Puntos repetidos (división por cero)."
                return self.raiz, historial

            delta0 = (f1 - f0) / h0
            delta1 = (f2 - f1) / h1

            a = (delta1 - delta0) / (h1 + h0)
            b = a * h1 + delta1
            c = f2

            # cmath permite manejar discriminantes negativos (raíces complejas)
            discriminante = cmath.sqrt(b**2 - 4 * a * c)

            # Se elige el denominador de mayor magnitud para mayor estabilidad
            if abs(b - discriminante) < abs(b + discriminante):
                denominador = b + discriminante
            else:
                denominador = b - discriminante

            if denominador == 0:
                self.convergio = False
                self.mensaje = "Error: División por cero en la fórmula de Müller."
                return self.raiz, historial

            p3 = p2 - (2 * c) / denominador

            # Si la parte imaginaria es despreciable, trabajamos con el real
            if isinstance(p3, complex) and abs(p3.imag) < self.tol:
                p3 = p3.real

            cota_error = abs(p3 - p2)

            historial.append({
                "iteracion": i,
                "p0": p0,
                "p1": p1,
                "p2": p2,
                "aproximacion": p3,
                "error": cota_error,
                "aprox": p3
            })

            if cota_error < self.tol:
                self.raiz = p3
                self.convergio = True
                self.mensaje = f"Convergió en {i+1} iteraciones con error {cota_error:.2e}."
                return self.raiz, historial

            # Actualización de los tres puntos
            p0, p1, p2 = p1, p2, p3
            f0, f1 = f1, f2
            f2 = self.f(p2)

        self.raiz = p3
        self.convergio = False
        self.mensaje = "Se alcanzó el máximo de iteraciones sin converger."
        return self.raiz, historial