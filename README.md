# Proyecto de Métodos Numéricos

Aplicación web interactiva para resolver problemas clásicos de análisis numérico con 7 módulos especializados: raíces de ecuaciones, interpolación, aproximación, derivación, integración, ecuaciones diferenciales ordinarias y simulaciones físicas.

Desarrollado por **Roony Roldan Cruz** — Instituto Politécnico Nacional, Escuela Superior de Cómputo.

---

## Módulos

| # | Módulo | Métodos implementados |
|---|---|---|
| 1 | **Ecuaciones No Lineales** | Bisección, Falsa Posición, Newton-Raphson, Secante, Punto Fijo, Müller |
| 2 | **Interpolación Polinomial** | Diferencias Divididas, Lagrange, Neville |
| 3 | **Aproximación de Funciones** | Mínimos Cuadrados Polinomial, Polinomios de Taylor |
| 4 | **Derivación Numérica** | Diferencias Finitas (3 y 5 puntos), Función analítica o datos tabulares |
| 5 | **Integración Numérica** | Trapecio, Simpson 1/3, Simpson 3/8 (simple y compuesta), Integral Doble, Gauss-Legendre, Adaptativa |
| 6 | **Ecuaciones Diferenciales** | Euler, Taylor (orden 2), Runge-Kutta 4, RKF45, Heun, Sistemas de n EDO |
| 7 | **Simulación Bungee** | Animación física de salto bungee (EDO de 2do orden con RK4) |

## Características

* **Interfaz:** construida con [Streamlit](https://streamlit.io/); cada módulo es una página independiente.
* **Arquitectura de 3 capas:** interfaz (`pages/`), lógica matemática (`src/metodos/`) y visualización (`src/graficador.py`) desacopladas.
* **Cálculo simbólico:** las funciones se ingresan como texto y se procesan con `sympy`.
* **Visualización:** gráficas con `matplotlib` para analizar convergencia, áreas, trayectorias y animaciones.
* **Entrada flexible:** acepta funciones analíticas (notación Python/sympy) y datos tabulares.

## Estructura del Proyecto

```text
metodos_numericos/
├── app.py                                      # Portada y configuración principal
├── pages/                                      # Interfaz de usuario (7 módulos)
│   ├── 01_Ecuaciones.py                        # Ecuaciones no lineales
│   ├── 02_Interpolacion.py                     # Interpolación polinomial
│   ├── 03_Aproximacion.py                      # Aproximación de funciones
│   ├── 04_Derivacion.py                        # Derivación numérica
│   ├── 05_Integracion.py                       # Integración numérica
│   ├── 06_Ecuaciones_Diferenciales.py          # Ecuaciones diferenciales
│   └── 07_Simulacion_Bungee.py                 # Simulación física
├── src/
│   ├── interface.py                            # Helpers de interfaz
│   ├── graficador.py                           # Clase Graficador (matplotlib)
│   └── metodos/                                # Backend matemático
│       ├── raices.py                           # SolucionadorRaices
│       ├── interpolacion.py                    # Interpolador
│       ├── aproximacion.py                     # Aproximador
│       ├── derivacion.py                       # DerivacionNumerica
│       ├── integracion.py                      # IntegracionNumerica
│       ├── edo.py                              # SolucionadorEDO, SolucionadorSistemasEDO
│       └── bungee.py                           # SimuladorBungee
├── CLAUDE.md                                   # Directrices de desarrollo
├── requirements.txt                            # Dependencias
└── README.md                                   # Este archivo
```

## Instalación y Ejecución

### 1. Requisitos previos

Tener instalado Python 3.8+ y pip. En Arch Linux:

```bash
sudo pacman -S python python-pip
```

### 2. Entorno virtual

Clona el repositorio (o sitúate en la carpeta del proyecto) y crea un entorno virtual:

```bash
python -m venv .venv
source .venv/bin/activate
```

### 3. Dependencias

Con el entorno activado:

```bash
pip install -r requirements.txt
```

### 4. Ejecución

```bash
streamlit run app.py
```

La aplicación se abre en el navegador (por defecto en `http://localhost:8501`). Selecciona un módulo en el menú lateral para comenzar.

## Uso rápido

1. **Elige un módulo** en el menú de la izquierda (7 opciones disponibles).
2. **Ingresa la función** en notación Python/sympy:
   - Ecuaciones: `x**2 - 4`, `sin(x) - x/2`
   - Integración: `x**3 + 2*x`, `exp(-x)`
   - Funciones multivariables: `x*y`, `sin(x)*cos(y)`
3. **Ajusta parámetros** (intervalos, tolerancia, paso, número de puntos, etc.).
4. **Presiona Calcular** para ver:
   - Métricas de convergencia/error
   - Tabla de iteraciones o resultados
   - Gráfica visualizando el proceso

## Convenciones de Desarrollo

El proyecto sigue las directrices documentadas en `CLAUDE.md`:
- **snake_case** para variables y funciones
- **Arquitectura de 3 capas** sin acoplamiento
- **Cálculo simbólico** con `sympy`, numérico con `numpy`
- **Interfaz exclusiva** de Streamlit
- **Modularidad** estricta

## Notas técnicas

- Las funciones se lambdifican internamente para evaluación rápida.
- Los métodos de raíces soportan raíces complejas (Müller, Newton con complejos).
- La integración adaptativa ajusta dinámicamente el paso según tolerancia.
- Las gráficas se generan dinámicamente según los datos y convergen a la mejor visualización del dominio.
