# Directrices de Desarrollo: Numerical-Methods

* **Arquitectura:** Respeta el patrón de 3 capas. Frontend (`app.py`, `pages/`), Backend Matemático (`src/metodos/`), y Visualización (`src/graficador.py`).
* **Convenciones:** Utiliza estrictamente `snake_case` para variables, funciones y atributos.
* **Lógica Matemática:** Usa `sympy` para el cálculo simbólico de derivadas. No implementes derivación numérica manual.
* **Interfaz:** La UI es exclusiva de `streamlit`. No introduzcas HTML/CSS a menos que sea estrictamente necesario con `st.markdown`.
* **Regla de Código:** Escribe código modular. Evita acoplar la lógica de cálculo en los archivos de la interfaz gráfica.

## Mapa del Sistema

### Estructura
- `app.py` — Página principal de Streamlit (presentación, sidebar con datos del autor).
- `pages/01_Ecuaciones.py` — UI de raíces: inputs globales (función, tolerancia, max_iter), selectbox de método, botón "Calcular", métricas, tabla de iteraciones y gráfica.
- `pages/02_Derivacion.py` — UI de derivación (incompleta, solo inputs).
- `src/metodos/raices.py` — Clase `SolucionadorRaices`. Métodos: `biseccion(a,b)`, `secante(p0,p1)`, `newton_rapshon(p0)`, `falsa_posicion(a,b)`, `punto_fijo(g_str,p0)`, `muller(p0,p1,p2)`.
- `src/metodos/derivacion.py` — Clase `Derivacion`.
- `src/interface.py` — `InterfaceHelper` (métodos estáticos): `inputs_metodo(metodo)` devuelve dict con los parámetros específicos de cada método; `mostrar_metricas(solver)`, `mostrar_tabla_iteraciones(historial)`, `encabezado_metodo()`, `encabezado_main()`.
- `src/graficador.py` — Clase `Graficador` (matplotlib): `graficar_funcion(f,a,b)`, `marcar_puntos(px,py)`, `obtener_figura()`.

### Contrato de los métodos de raíces
Todos los métodos de `SolucionadorRaices` siguen el mismo patrón:
1. Reciben los parámetros iniciales y devuelven `(raiz, historial)`.
2. `historial` es una lista de dicts por iteración; debe incluir la clave `"aprox"` (la usa la página para marcar puntos en la gráfica). El resto de claves se muestran tal cual en la tabla.
3. Setean `self.raiz`, `self.convergio` (bool) y `self.mensaje` (los lee `mostrar_metricas`).
4. El constructor lambdifica `f` y `f'` con sympy/numpy (`self.f`, `self.derivada_f`), guarda `self.tol` y `self.max_iter`.

### Para agregar un método nuevo de raíces (3 pasos)
1. Implementar el método en `SolucionadorRaices` respetando el contrato anterior.
2. Agregar branch en `InterfaceHelper.inputs_metodo()` con los inputs específicos.
3. En `pages/01_Ecuaciones.py`: agregar el nombre al `selectbox` y un `elif` que llame al método con las claves del dict de inputs.

### Notas
- Entorno virtual: `.venv/` (usar `.venv/bin/python` para ejecutar/probar). Correr app: `.venv/bin/streamlit run app.py`.
- `muller` usa `cmath` y puede devolver raíces complejas; la página grafica solo la parte real de las aproximaciones. `st.metric` formatea complejos sin problema (`f"{raiz:.10f}"` funciona con complex).
- El rango de la gráfica se calcula con `min/max` de los inputs numéricos `± 3` (se filtran strings como g(x)).
- `punto_fijo` recibe g(x) como string aparte y la lambdifica internamente; f(x) solo se usa para verificar `f(p1)` en la tabla.
