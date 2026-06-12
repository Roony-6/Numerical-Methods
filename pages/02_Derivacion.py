import streamlit as st
import pandas as pd
from src.metodos.derivacion import DerivacionNumerica
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo(
    "Diferenciación Numérica",
    "Aproxima f'(x) con fórmulas de diferencias finitas de 3 y 5 puntos"
)

modo = st.radio("Tipo de entrada:", ["Función Analítica", "Datos Tabulares"], horizontal=True)

if modo == "Función Analítica":
    c1, c2, c3, c4 = st.columns(4)
    funcion = c1.text_input("Función f(x):", "x**2 - 4")
    a = c2.number_input("a:", value=0.0)
    b = c3.number_input("b:", value=5.0)
    n = c4.number_input("Subintervalos (n):", value=10, min_value=2, step=1)
else:
    st.write("Ingresa los puntos (x debe estar uniformemente espaciado):")
    datos_default = pd.DataFrame({
        "x": [0.0, 0.5, 1.0, 1.5, 2.0],
        "y": [0.0, 0.25, 1.0, 2.25, 4.0],
    })
    datos = st.data_editor(datos_default, num_rows="dynamic", use_container_width=True)

if st.button("Calcular", type="primary"):
    try:
        if modo == "Función Analítica":
            solver = DerivacionNumerica.desde_funcion(funcion, a, b, int(n))
        else:
            datos_limpios = datos.dropna()
            solver = DerivacionNumerica(datos_limpios["x"], datos_limpios["y"])

        df_resultados = solver.calcular_derivadas()

        st.subheader("Tabla de resultados")
        st.dataframe(df_resultados, use_container_width=True)

        graficador = Graficador("f(x) y su derivada aproximada")
        figura = graficador.graficar_derivada(df_resultados)
        st.pyplot(figura)
    except Exception as e:
        st.error(f"Error en el cálculo: {e}")
