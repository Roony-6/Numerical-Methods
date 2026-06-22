import numpy as np
from sympy import sympify, symbols, lambdify


class IntegracionNumerica:
    def __init__(self, funcion_str):
        x_sym = symbols('x')
        self.f = lambdify(x_sym, sympify(funcion_str), modules="numpy")

    def _evaluar(self, nodos):
        return np.array([self.f(p) for p in nodos], dtype=float)

    # --- Integración simple ---
    def regla_trapecio(self, a, b):
        h = b - a
        nodos = [a, b]
        y = self._evaluar(nodos)
        valor = (h / 2) * (y[0] + y[1])
        return valor, {"metodo": "Trapecio", "h": h, "nodos": nodos}

    def regla_simpson_1_3(self, a, b):
        h = (b - a) / 2
        nodos = [a, a + h, b]
        y = self._evaluar(nodos)
        valor = (h / 3) * (y[0] + 4 * y[1] + y[2])
        return valor, {"metodo": "Simpson 1/3", "h": h, "nodos": nodos}

    def regla_simpson_3_8(self, a, b):
        h = (b - a) / 3
        nodos = [a, a + h, a + 2 * h, b]
        y = self._evaluar(nodos)
        valor = (3 * h / 8) * (y[0] + 3 * y[1] + 3 * y[2] + y[3])
        return valor, {"metodo": "Simpson 3/8", "h": h, "nodos": nodos}


    # --- Integración compuesta ---
    def trapecio_compuesta(self, a, b, n):
        n = self._validar_n(n)
        h = (b - a) / n
        nodos = np.linspace(a, b, n + 1)
        y = self._evaluar(nodos)
        valor = (h / 2) * (y[0] + 2 * y[1:-1].sum() + y[-1])
        return valor, {"metodo": "Trapecio Compuesta", "h": h, "n": n, "nodos": nodos.tolist()}

    def simpson_1_3_compuesta(self, a, b, n):
        n = self._validar_n(n)
        if n % 2 != 0:
            raise ValueError("Simpson 1/3 compuesta requiere un número par de subintervalos (n).")
        h = (b - a) / n
        nodos = np.linspace(a, b, n + 1)
        y = self._evaluar(nodos)
        valor = (h / 3) * (y[0] + 4 * y[1:-1:2].sum() + 2 * y[2:-1:2].sum() + y[-1])
        return valor, {"metodo": "Simpson 1/3 Compuesta", "h": h, "n": n, "nodos": nodos.tolist()}

    def simpson_3_8_compuesta(self, a, b, n):
        n = self._validar_n(n)
        if n % 3 != 0:
            raise ValueError("Simpson 3/8 compuesta requiere que n sea múltiplo de 3.")
        h = (b - a) / n
        nodos = np.linspace(a, b, n + 1)
        y = self._evaluar(nodos)
        suma_no_multiplos = sum(y[i] for i in range(1, n) if i % 3 != 0)
        suma_multiplos = sum(y[i] for i in range(3, n, 3))
        valor = (3 * h / 8) * (y[0] + 3 * suma_no_multiplos + 2 * suma_multiplos + y[-1])
        return valor, {"metodo": "Simpson 3/8 Compuesta", "h": h, "n": n, "nodos": nodos.tolist()}


    # --- Integración múltiple ---
    @staticmethod
    def integral_doble_simpson(funcion_xy_str, a, b, c, d, n=10, m=10):
        """Integral doble sobre el rectángulo [a,b]x[c,d] con Simpson 1/3 compuesta en ambos ejes."""
        n, m = int(n), int(m)
        if n % 2 != 0 or m % 2 != 0:
            raise ValueError("n y m deben ser pares para Simpson 1/3.")
        x_sym, y_sym = symbols('x y')
        f_xy = lambdify((x_sym, y_sym), sympify(funcion_xy_str), modules="numpy")

        h_x = (b - a) / n
        h_y = (d - c) / m
        nodos_x = np.linspace(a, b, n + 1)
        nodos_y = np.linspace(c, d, m + 1)

        def peso_simpson(indice, total):
            if indice == 0 or indice == total:
                return 1
            return 4 if indice % 2 == 1 else 2

        valor = 0.0
        for i, xi in enumerate(nodos_x):
            for j, yj in enumerate(nodos_y):
                valor += peso_simpson(i, n) * peso_simpson(j, m) * f_xy(xi, yj)
        valor *= h_x * h_y / 9

        return valor, {
            "metodo": "Integral Doble (Simpson 1/3)",
            "h_x": h_x, "h_y": h_y, "n": n, "m": m,
            "nodos_x": nodos_x.tolist(), "nodos_y": nodos_y.tolist(),
        }

    def integral_gaussiana(self, a, b, n_puntos=2):
        """Cuadratura de Gauss-Legendre en [a, b] con n_puntos nodos."""
        n_puntos = int(n_puntos)
        if n_puntos < 1:
            raise ValueError("Se requiere al menos 1 punto de Gauss.")
        raices, pesos = np.polynomial.legendre.leggauss(n_puntos)
        nodos = 0.5 * (b - a) * raices + 0.5 * (a + b)
        valor = 0.5 * (b - a) * np.sum(pesos * self._evaluar(nodos))
        return valor, {
            "metodo": f"Cuadratura Gaussiana ({n_puntos} puntos)",
            "nodos": nodos.tolist(),
            "pesos": pesos.tolist(),
        }

    def cuadratura_gauss_legendre(self, a, b, n_puntos):
        """
        Cuadratura de Gauss-Legendre en [a, b] con n_puntos nodos.

        Args:
            a: límite inferior
            b: límite superior
            n_puntos: número de puntos de Gauss

        Returns:
            (valor_integral, detalles)
        """
        return self.integral_gaussiana(a, b, n_puntos)

    def cuadratura_adaptativa(self, a, b, tol):
        """
        Integración adaptativa usando Simpson 1/3 recursivo.

        Args:
            a: límite inferior
            b: límite superior
            tol: tolerancia de error

        Returns:
            (valor_integral, detalles)
        """
        puntos_evaluados = []

        def simpson_adaptativo(a, b, tol, nivel=0):
            h = b - a
            c = (a + b) / 2

            fa = self.f(a)
            fc = self.f(c)
            fb = self.f(b)

            puntos_evaluados.extend([a, c, b])

            simpson_completo = (h / 6) * (fa + 4 * fc + fb)

            if nivel == 0:
                c1 = (a + c) / 2
                c2 = (c + b) / 2
                fc1 = self.f(c1)
                fc2 = self.f(c2)
                puntos_evaluados.extend([c1, c2])

                simpson_izq = ((c - a) / 6) * (fa + 4 * fc1 + fc)
                simpson_der = ((b - c) / 6) * (fc + 4 * fc2 + fb)
                simpson_doble = simpson_izq + simpson_der

                error = abs(simpson_doble - simpson_completo) / 15.0

                if error < tol:
                    return simpson_doble
                else:
                    izq = simpson_adaptativo(a, c, tol / 2, nivel + 1)
                    der = simpson_adaptativo(c, b, tol / 2, nivel + 1)
                    return izq + der
            else:
                c1 = (a + c) / 2
                c2 = (c + b) / 2
                fc1 = self.f(c1)
                fc2 = self.f(c2)
                puntos_evaluados.extend([c1, c2])

                simpson_izq = ((c - a) / 6) * (fa + 4 * fc1 + fc)
                simpson_der = ((b - c) / 6) * (fc + 4 * fc2 + fb)
                simpson_doble = simpson_izq + simpson_der

                error = abs(simpson_doble - simpson_completo) / 15.0

                if error < tol:
                    return simpson_doble
                else:
                    izq = simpson_adaptativo(a, c, tol / 2, nivel + 1)
                    der = simpson_adaptativo(c, b, tol / 2, nivel + 1)
                    return izq + der

        valor = simpson_adaptativo(a, b, tol)
        puntos_evaluados_unicos = sorted(list(set(np.round(puntos_evaluados, 12))))

        return valor, {
            "metodo": "Integración Adaptativa (Simpson 1/3)",
            "tolerancia": tol,
            "nodos": puntos_evaluados_unicos
        }

    @staticmethod
    def _validar_n(n):
        n = int(n)
        if n < 1:
            raise ValueError("El número de subintervalos n debe ser al menos 1.")
        return n
