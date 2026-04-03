class SolucionadorRaices:
    def __init__(self, function, tol = 1e-6, max_iter=100):
        self.f = lambda x: eval(function)
        self.tol = tol
        self.max_iter = max_iter
        
        #Resultados despues de la ejecucion
        self.raiz = None
        self.convergio = False
        self.mensaje = ""
        
    
    def biseccion(self, a:float, b:float)->float:
        historial = []
        
        if self.f(a) * self.f(b) >= 0:
            self.convergio = False
            self.mensaje = (
                f"No hay cambio de signo en [{a}, {b}]. "
                "Ajusta el intervalo para que f(a) y f(b) tengan signos opuestos."
            )
            return historial
        c_anterior = None
        
        for i in range (self.max_iter):
            c_actual = (a + b) / 2
            fa = self.f(a)
            fb = self.f(b)
            fc = self.f(c_actual)
            producto = fa * fc
            cota_error = abs(c_actual - c_anterior) if c_anterior is not None else None
            
            fila = {"iteraciones": i,
                    "a": a, 
                    "b": b,
                    "c": c_actual,
                    "f(a)": fa,
                    "f(c)": fc,
                    "f(b)": fb,
                    "error": cota_error}
            
            historial.append(fila)
            
            #--Criterios de paro--
            
            if c_actual == 0: # Raiz exacta encontrada
                self.raiz = c_actual
                self.convergio = True
                self.mensaje = f"Raíz exacta encontrada en la iteración {i}."
                break
            
            if cota_error is not None and cota_error < self.tol:
                self.raiz = c_actual
                self.convergio = True
                self.mensaje = f"Convergió en {i} iteraciones (error = {cota_error:.2e})."
                break
            
            # --- Actualizar intervalo ---
            if producto < 0:
                b = c_actual  # Raíz en la mitad izquierda [a, c]
            else:
                a = c_actual   # Raíz en la mitad derecha  [c, b]

            c_anterior = c_actual

        else:
            # Se agotaron las iteraciones sin converger
            self.raiz = c_actual
            self.convergio = False
            self.mensaje = (
                f"Se alcanzó el máximo de {self.max_iter} iteraciones sin converger. "
                f"Última aproximación: {c_anterior:.8f}"
            )

        return self.raiz,historial
            
    
    def secante(self, p0: float, p1: float):
        historial = []
        
        f0 = self.f(p0)
        f1 = self.f(p1) 

        for i in range(self.max_iter):
        
            if (f1 - f0) == 0:
                self.mensaje = "Error: División por cero (f(p1) - f(p0) = 0)."
                break

            p2 = p1 - (f1 * (p1 - p0)) / (f1 - f0)


            error_relativo = abs(p2 - p1)

            fila = {
                "iteraciones": i,
                "p0": p0,
                "p1": p1,
                "aproximacion": p2,
                "cota error": error_relativo
            }
            historial.append(fila)

            if error_relativo < self.tol:
                self.raiz = p2
                self.convergio = True
                self.mensaje = f"Convergió en {i} iteraciones (error = {error_relativo:.2e})."
                break
            
            # 4. ACTUALIZACIÓN CRÍTICA
            p0 = p1
            f0 = f1 # Guardamos el valor actual para la siguiente vuelta
            p1 = p2
            f1 = self.f(p1) # Evaluamos el nuevo punto

        else:
            self.raiz = p1
            self.convergio = False
            self.mensaje = f"Se alcanzó el máximo de iteraciones sin converger."
        return self.raiz,historial