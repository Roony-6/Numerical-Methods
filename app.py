import streamlit as st
from src.interface import InterfaceHelper


# 1. Configuración 
st.set_page_config(
    page_title="Proyecto Metodos Numericos",
    page_icon="R",
    layout="wide"
)

# 2. Título y Bienvenida

InterfaceHelper.encabezado_main("Proyecto Metodos Numericos", "Aplicacion para encontrar raices con metodos "
                                "numericos iterarativos y mas")

# 3. Información del Estudiante (Presentación)
with st.sidebar:
    st.info(" **Roony Roldan Cruz** \n\n **Institucion:** Instituto Politecnico Nacional \n\n **Universidad:** Escuela Superior de Computo")

# 4. Contenido Principal
col1, col2 = st.columns([2, 1])

with col1:
    st.write("""
    ### Calculadora de raices 
    Esta aplicación permite resolver problemas complejos para encontrar raices con 
    la implementación de algoritmos matemáticos **.
    
    **Secciones disponibles:**
    * **Raíces de Ecuaciones:** Bisección, Newton-Raphson, Secante,etc.
    **Por desarrollar:**
    * **Interpolación:** Lagrange, Newton (Diferencias Divididas).
    * **Aproximaciones** Polinomios por minimos cuadrados
    * **Derivacion:** Derivacion numerica
    * **Integración:** Regla del Trapecio y Simpson.
    """)
    
    # Ejemplo de fórmula en LaTeX
    #st.latex(r"f(x) = \sum_{i=0}^{n} y_i L_i(x)")

#with col2:
    #st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png", width=150)

st.success(" <- Selecciona un método en el menú de la izquierda para comenzar.")