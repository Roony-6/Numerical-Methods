class SolucionadorRaices:
    def __init__(self, function, tol = 1e-6, max_iter=100):
        self.f = lambda x: eval(function)
        self.tol = tol
        self.max_itier = max_iter
        
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
        
        for i in range (self.max_itier):
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
                f"Se alcanzó el máximo de {self.max_itier} iteraciones sin converger. "
                f"Última aproximación: {c_anterior:.8f}"
            )

        return historial
            
                
            
            
        
        
        
        