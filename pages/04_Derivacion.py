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
    col1, col2, col3 = st.columns(3)
    with col1:
        funcion = st.text_input("f(x):", value="x**2 - 4", placeholder="ej: x**2, sin(x)")
    with col2:
        metodo_deriv = st.selectbox("Metodo:", ["Diferencias Finitas", "Richardson"], label_visibility="collapsed")
    with col3:
        x_eval = st.number_input("Punto x para derivar:", value=1.0)

    if metodo_deriv == "Diferencias Finitas":
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            a = st.number_input("Limite a:", value=0.0)
        with col2:
            b = st.number_input("Limite b:", value=5.0)
        with col3:
            n = st.number_input("Subintervalos (n):", value=10, min_value=2, step=1)
        with col4:
            st.empty()
    else:  # Richardson
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            h_inicial = st.number_input("Paso h inicial:", value=0.1, format="%.6f")
        with col2:
            tol_richardson = st.number_input("Tolerancia:", value=1e-6, format="%.2e")
        with col3:
            max_iter_richardson = st.number_input("Max iteraciones:", value=20, min_value=1, step=1)
        with col4:
            st.empty()

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
            if metodo_deriv == "Diferencias Finitas":
                solver = DerivacionNumerica.desde_funcion(funcion, a, b, int(n))
                df_resultados = solver.calcular_derivadas()

                st.success("Derivadas calculadas exitosamente")

                st.subheader("Tabla de resultados")
                st.dataframe(df_resultados, use_container_width=True)

                st.subheader("Grafica")
                graficador = Graficador("f(x) y su derivada aproximada")
                figura = graficador.graficar_derivada(df_resultados)
                st.pyplot(figura)

            else:  # Richardson
                from sympy import symbols, lambdify, sympify
                x_sym = symbols('x')
                f = lambdify(x_sym, sympify(funcion), modules="numpy")

                derivada, tabla_richardson, historial, convergio = DerivacionNumerica.richardson(
                    f, x_eval, h_inicial, tol=tol_richardson, max_iter=max_iter_richardson
                )

                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Derivada aproximada", f"{derivada:.10f}")
                with col2:
                    st.metric("Punto evaluado", f"x = {x_eval}")
                with col3:
                    estado = "✓ Convergió" if convergio else "✗ No convergió"
                    st.metric("Estado", estado)

                st.subheader("Historial de convergencia")
                df_historial = pd.DataFrame(historial)
                st.dataframe(df_historial, use_container_width=True)

                st.subheader("Tabla de Richardson")
                tabla_str = "Tabla de Richardson (primeras 5 iteraciones):\n"
                for i in range(min(5, len(tabla_richardson))):
                    fila = [f"{tabla_richardson[i][j]:.10f}" if j < len(tabla_richardson[i]) else ""
                            for j in range(min(6, len(tabla_richardson[i])))]
                    tabla_str += "  ".join(fila) + "\n"
                st.code(tabla_str)

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
