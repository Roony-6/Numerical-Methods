import numpy as np
import pandas as pd
from sympy import sympify, symbols, diff, lambdify


class SolucionadorEDO:
    def __init__(self, funcion_str):
        x_sym, y_sym = symbols('x y')
        expr_f = sympify(funcion_str)
        self.f = lambdify((x_sym, y_sym), expr_f, modules="numpy")

        # Derivada total de f respecto a x (regla de la cadena): f' = f_x + f_y * f
        expr_df = diff(expr_f, x_sym) + diff(expr_f, y_sym) * expr_f
        self.df_total = lambdify((x_sym, y_sym), expr_df, modules="numpy")

    @staticmethod
    def _construir_dataframe(historial):
        return pd.DataFrame(historial, columns=['Iteración', 'x', 'y_aprox', 'h_usado'])

    def metodo_euler(self, x0, y0, xf, h):
        x, y = x0, y0
        historial = [{'Iteración': 0, 'x': x, 'y_aprox': y, 'h_usado': h}]
        i = 0
        while x < xf - 1e-12:
            h_paso = min(h, xf - x)
            y = y + h_paso * self.f(x, y)
            x = x + h_paso
            i += 1
            historial.append({'Iteración': i, 'x': x, 'y_aprox': y, 'h_usado': h_paso})
        return self._construir_dataframe(historial)

    def metodo_taylor_orden_2(self, x0, y0, xf, h):
        x, y = x0, y0
        historial = [{'Iteración': 0, 'x': x, 'y_aprox': y, 'h_usado': h}]
        i = 0
        while x < xf - 1e-12:
            h_paso = min(h, xf - x)
            y = y + h_paso * self.f(x, y) + (h_paso ** 2 / 2) * self.df_total(x, y)
            x = x + h_paso
            i += 1
            historial.append({'Iteración': i, 'x': x, 'y_aprox': y, 'h_usado': h_paso})
        return self._construir_dataframe(historial)

    def runge_kutta_4(self, x0, y0, xf, h):
        x, y = x0, y0
        historial = [{'Iteración': 0, 'x': x, 'y_aprox': y, 'h_usado': h}]
        i = 0
        while x < xf - 1e-12:
            h_paso = min(h, xf - x)
            k1 = self.f(x, y)
            k2 = self.f(x + h_paso / 2, y + h_paso * k1 / 2)
            k3 = self.f(x + h_paso / 2, y + h_paso * k2 / 2)
            k4 = self.f(x + h_paso, y + h_paso * k3)
            y = y + (h_paso / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            x = x + h_paso
            i += 1
            historial.append({'Iteración': i, 'x': x, 'y_aprox': y, 'h_usado': h_paso})
        return self._construir_dataframe(historial)

    def metodo_heun(self, x0, y0, xf, h):
        x, y = x0, y0
        historial = [{'Iteración': 0, 'x': x, 'y_aprox': y, 'h_usado': h}]
        i = 0
        while x < xf - 1e-12:
            h_paso = min(h, xf - x)
            k1 = self.f(x, y)
            k2 = self.f(x + h_paso, y + h_paso * k1)
            y = y + (h_paso / 2) * (k1 + k2)
            x = x + h_paso
            i += 1
            historial.append({'Iteración': i, 'x': x, 'y_aprox': y, 'h_usado': h_paso})
        return self._construir_dataframe(historial)

    def runge_kutta_fehlberg(self, x0, y0, xf, tol, h_min, h_max):
        x, y = x0, y0
        h = h_max
        historial = [{'Iteración': 0, 'x': x, 'y_aprox': y, 'h_usado': h}]
        i = 0
        while x < xf - 1e-12:
            h = min(h, xf - x)

            k1 = h * self.f(x, y)
            k2 = h * self.f(x + h / 4, y + k1 / 4)
            k3 = h * self.f(x + 3 * h / 8, y + 3 * k1 / 32 + 9 * k2 / 32)
            k4 = h * self.f(x + 12 * h / 13,
                            y + 1932 * k1 / 2197 - 7200 * k2 / 2197 + 7296 * k3 / 2197)
            k5 = h * self.f(x + h,
                            y + 439 * k1 / 216 - 8 * k2 + 3680 * k3 / 513 - 845 * k4 / 4104)
            k6 = h * self.f(x + h / 2,
                            y - 8 * k1 / 27 + 2 * k2 - 3544 * k3 / 2565
                            + 1859 * k4 / 4104 - 11 * k5 / 40)

            # Error local: diferencia entre la aproximación de orden 5 y la de orden 4
            error = abs(k1 / 360 - 128 * k3 / 4275 - 2197 * k4 / 75240
                        + k5 / 50 + 2 * k6 / 55)

            if error <= tol or h <= h_min:
                y = y + 25 * k1 / 216 + 1408 * k3 / 2565 + 2197 * k4 / 4104 - k5 / 5
                x = x + h
                i += 1
                historial.append({'Iteración': i, 'x': x, 'y_aprox': y, 'h_usado': h})

            # Factor de ajuste del paso (0.84 ~ (1/2)^(1/4) de seguridad)
            if error > 0:
                delta = 0.84 * (tol / error) ** 0.25
                delta = max(0.1, min(delta, 4.0))
            else:
                delta = 4.0
            h = max(h_min, min(h * delta, h_max))

        return self._construir_dataframe(historial)


class SolucionadorSistemasEDO:
    def __init__(self, funciones_str):
        self.n = len(funciones_str)
        x_sym = symbols('x')
        y_syms = symbols(f'y1:{self.n + 1}')
        self.funciones = [
            lambdify((x_sym, *y_syms), sympify(f_str), modules="numpy")
            for f_str in funciones_str
        ]
        self.columnas_y = [f'y{i + 1}' for i in range(self.n)]

    def _evaluar(self, x, y):
        return np.array([f(x, *y) for f in self.funciones], dtype=float)

    def runge_kutta_4_sistemas(self, x0, y0, xf, h):
        x = x0
        y = np.array(y0, dtype=float)
        historial = [{'Iteración': 0, 'x': x, **dict(zip(self.columnas_y, y)), 'h_usado': h}]
        i = 0
        while x < xf - 1e-12:
            h_paso = min(h, xf - x)
            k1 = self._evaluar(x, y)
            k2 = self._evaluar(x + h_paso / 2, y + h_paso * k1 / 2)
            k3 = self._evaluar(x + h_paso / 2, y + h_paso * k2 / 2)
            k4 = self._evaluar(x + h_paso, y + h_paso * k3)
            y = y + (h_paso / 6) * (k1 + 2 * k2 + 2 * k3 + k4)
            x = x + h_paso
            i += 1
            historial.append({'Iteración': i, 'x': x, **dict(zip(self.columnas_y, y)),
                              'h_usado': h_paso})
        return pd.DataFrame(historial, columns=['Iteración', 'x', *self.columnas_y, 'h_usado'])
