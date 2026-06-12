# Proyecto de Métodos Numéricos

Aplicación web interactiva para resolver problemas clásicos de análisis numérico: raíces de ecuaciones, derivación, integración, ecuaciones diferenciales ordinarias y simulaciones físicas.

Desarrollado por **Roony Roldan Cruz** — Instituto Politécnico Nacional, Escuela Superior de Cómputo.

---

## Módulos

| Módulo | Métodos implementados |
|---|---|
| **Raíces de Ecuaciones** | Bisección, Falsa Posición, Newton-Raphson, Secante, Punto Fijo, Müller |
| **Derivación Numérica** | Diferencias finitas (función analítica o datos tabulares), Extrapolación de Richardson |
| **Integración Numérica** | Trapecio, Simpson 1/3, Simpson 3/8 y Punto Medio (simples y compuestas), Integral doble, Cuadratura Gaussiana |
| **Ecuaciones Diferenciales** | Euler, Taylor (orden 2), RK4, RKF45 (paso adaptativo), Adams-Bashforth-Moulton (predictor-corrector), RK4 para sistemas de n EDO |
| **Simulación Bungee** | Animación de un salto en bungee modelado como EDO de 2do orden resuelta con RK4 |

## Características

* **Interfaz:** construida con [Streamlit](https://streamlit.io/); cada módulo es una página independiente.
* **Arquitectura de 3 capas:** interfaz (`pages/`), lógica matemática (`src/metodos/`) y visualización (`src/graficador.py`) desacopladas.
* **Cálculo simbólico:** las funciones se ingresan como texto y se procesan con `sympy`.
* **Visualización:** gráficas con `matplotlib` para analizar convergencia, áreas, trayectorias y animaciones.

## Estructura del Proyecto

```text
metodos_numericos/
├── app.py                              # Portada y configuración principal
├── pages/                              # Interfaz de usuario (una página por módulo)
│   ├── 01_Ecuaciones.py                # Raíces de ecuaciones
│   ├── 02_Derivacion.py                # Derivación numérica
│   ├── 03_Integracion.py               # Integración numérica
│   ├── 04_Ecuaciones_Diferenciales.py  # EDO: valor inicial, multipaso y sistemas
│   └── 05_Simulacion_Bungee.py         # Simulación animada de salto bungee
├── src/
│   ├── interface.py                    # Helpers de interfaz (inputs, métricas, tablas)
│   ├── graficador.py                   # Clase Graficador (matplotlib)
│   └── metodos/                        # Lógica matemática
│       ├── raices.py                   # SolucionadorRaices
│       ├── derivacion.py               # DerivacionNumerica
│       ├── integracion.py              # IntegracionNumerica
│       ├── edo.py                      # SolucionadorEDO y SolucionadorSistemasEDO
│       └── bungee.py                   # SimuladorBungee
├── requirements.txt                    # Dependencias del proyecto
└── README.md                           # Documentación (este archivo)
```

## Instalación y Ejecución

### 1. Requisitos previos

Tener instalado Python 3 y pip. En Arch Linux:

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

Con el entorno activado (verás `(.venv)` en tu terminal):

```bash
pip install -r requirements.txt
```

### 4. Ejecución

```bash
streamlit run app.py
```

La aplicación se abre en el navegador (por defecto en `http://localhost:8501`). Selecciona un módulo en el menú lateral para comenzar.

## Uso rápido

1. Elige un módulo en el menú de la izquierda.
2. Escribe la función en notación Python/sympy (ej. `x**2 - 4`, `exp(-x)*sin(x)`, `x + y`).
3. Ajusta los parámetros del método (intervalos, tolerancia, paso, etc.).
4. Presiona **Calcular** para ver métricas, tabla de iteraciones y gráfica.
