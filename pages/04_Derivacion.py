import streamlit as st
import pandas as pd
from src.metodos.derivacion import DerivacionNumerica
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo(
    "Diferenciacion Numerica",
    "Aproxima f'(x) con formulas de diferencias finitas de 3 y 5 puntos"
)

st.subheader("Tipo de entrada")
modo = st.radio("Selecciona la fuente de datos:", ["Funcion Analitica", "Datos Tabulares"], horizontal=True)

if modo == "Funcion Analitica":
    st.subheader("Parametros de la funcion")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        funcion = st.text_input("f(x):", value="x**2 - 4", placeholder="ej: x**2, sin(x)")
    with col2:
        a = st.number_input("Limite a:", value=0.0)
    with col3:
        b = st.number_input("Limite b:", value=5.0)
    with col4:
        n = st.number_input("Subintervalos (n):", value=10, min_value=2, step=1)

else:
    st.subheader("Datos tabulares")
    st.write("Ingresa los puntos (x debe estar uniformemente espaciado):")
    datos_default = pd.DataFrame({
        "x": [0.0, 0.5, 1.0, 1.5, 2.0],
        "y": [0.0, 0.25, 1.0, 2.25, 4.0],
    })
    datos = st.data_editor(datos_default, num_rows="dynamic", use_container_width=True)

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.empty()
with col2:
    st.empty()
with col3:
    btn_calc = st.button("Calcular", type="primary", use_container_width=True)

if btn_calc:
    try:
        if modo == "Funcion Analitica":
            solver = DerivacionNumerica.desde_funcion(funcion, a, b, int(n))
        else:
            datos_limpios = datos.dropna()
            solver = DerivacionNumerica(datos_limpios["x"], datos_limpios["y"])

        df_resultados = solver.calcular_derivadas()

        st.success("Derivadas calculadas exitosamente")

        st.subheader("Tabla de resultados")
        st.dataframe(df_resultados, use_container_width=True)

        st.subheader("Grafica")
        graficador = Graficador("f(x) y su derivada aproximada")
        figura = graficador.graficar_derivada(df_resultados)
        st.pyplot(figura)

    except Exception as e:
        st.error(f"Error en el calculo: {e}")
