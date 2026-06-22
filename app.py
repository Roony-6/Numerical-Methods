import streamlit as st
from src.interface import InterfaceHelper

st.set_page_config(
    page_title="Metodos Numericos",
    page_icon="λ",
    layout="wide"
)

InterfaceHelper.encabezado_main(
    "Metodos Numericos",
    "Aplicacion para resolver problemas matematicos con metodos numericos"
)

with st.sidebar:
    st.info(
        "**Roony Roldan Cruz**\n\n"
        "**Institucion:** Instituto Politecnico Nacional\n\n"
        "**Escuela:** Escuela Superior de Computo"
    )

col1, col2 = st.columns([3, 1])

with col1:
    st.subheader("Modulos Disponibles")
    st.write("""
    Esta aplicacion implementa algoritmos numericos para resolver diversos problemas matematicos.
    Selecciona un modulo en el menu lateral para comenzar.

    **Modulos implementados:**

    1. **Ecuaciones No Lineales** - Encuentra raices de ecuaciones
       - Bisección, Falsa Posición, Secante, Newton-Raphson, Müller, Punto Fijo

    2. **Interpolacion Polinomial** - Interpola datos mediante polinomios
       - Diferencias Divididas, Lagrange, Neville

    3. **Aproximacion de Funciones** - Ajusta funciones a datos
       - Minimos Cuadrados Polinomial, Polinomios de Taylor

    4. **Derivacion Numerica** - Calcula derivadas aproximadas
       - Diferencias Finitas, Derivadas de orden superior

    5. **Integracion Numerica** - Aproxima integrales definidas
       - Simple (Trapecio, Simpson 1/3, Simpson 3/8)
       - Compuesta (Trapecio, Simpson 1/3, Simpson 3/8)
       - Integral Doble, Gauss-Legendre, Adaptativa

    6. **Ecuaciones Diferenciales** - Resuelve EDO y sistemas
       - Euler, Taylor (Orden 2), Runge-Kutta 4, RKF45, Heun

    7. **Simulacion Bungee** - Simulacion fisica del salto bungee
       - Runge-Kutta 4 con visualizacion
    """)

st.divider()

st.success("Selecciona un modulo en el menu de la izquierda para comenzar.")
