import streamlit as st
import numpy as np
import pandas as pd
from sympy import symbols, lambdify
from src.metodos.interpolacion import Interpolador
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo("Interpolación Polinomial",
                                  "Interpola datos usando Diferencias Divididas, Lagrange o Neville")

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Datos de entrada")
with col2:
    n_puntos = st.number_input("Cantidad de puntos:", value=3, min_value=2, max_value=20, label_visibility="collapsed")

datos_df = pd.DataFrame({
    'x': [float(i) for i in range(n_puntos)],
    'y': [float(i**2) for i in range(n_puntos)]
})

datos_editado = st.data_editor(datos_df, num_rows="dynamic", key="datos_interpolacion", use_container_width=True)

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    metodo = st.selectbox("Metodo de interpolacion:",
                         ["Diferencias Divididas", "Lagrange", "Neville"], label_visibility="collapsed")
with col2:
    if metodo == "Neville":
        x_target = st.number_input("Valor x:", value=0.5, label_visibility="collapsed")
    else:
        x_target = None
with col3:
    btn_calc = st.button("Calcular", type="primary", use_container_width=True)

if btn_calc:
    try:
        x_vals = datos_editado['x'].values
        y_vals = datos_editado['y'].values

        interpolador = Interpolador(x_vals, y_vals)

        if metodo == "Diferencias Divididas":
            polinomio, tabla, f_newton = interpolador.diferencias_divididas()
            st.success("Polinomio calculado mediante Diferencias Divididas")

            st.subheader("Polinomio resultante:")
            st.latex(f"P(x) = {polinomio}")

            InterfaceHelper.mostrar_tabla_diferencias(tabla, x_vals)

        elif metodo == "Lagrange":
            polinomio = interpolador.lagrange()
            st.success("Polinomio de Lagrange calculado")

            st.subheader("Polinomio resultante:")
            st.latex(f"P(x) = {polinomio}")

        elif metodo == "Neville":
            valor, matriz = interpolador.neville(x_target)
            st.success("Valor interpolado mediante Algoritmo de Neville")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Valor interpolado", f"{valor:.10f}")
            with col2:
                st.metric("Punto evaluado", f"x = {x_target}")

            with st.expander("Ver matriz de Neville"):
                df_neville = pd.DataFrame(matriz)
                st.dataframe(df_neville, use_container_width=True)

        grafica = Graficador(titulo=f"Interpolacion - {metodo}")

        grafica.ax.scatter(x_vals, y_vals, color='red', s=100, label='Datos', zorder=5)

        if metodo == "Diferencias Divididas":
            x_continuo = np.linspace(min(x_vals) - 1, max(x_vals) + 1, 200)
            y_continuo = f_newton(x_continuo)
            grafica.ax.plot(x_continuo, y_continuo, label='Polinomio', color='blue', linewidth=2)
        elif metodo == "Lagrange":
            x = symbols('x')
            f_poly = lambdify(x, polinomio, 'numpy')
            x_continuo = np.linspace(min(x_vals) - 1, max(x_vals) + 1, 200)
            y_continuo = f_poly(x_continuo)
            grafica.ax.plot(x_continuo, y_continuo, label='Polinomio', color='blue', linewidth=2)
        else:
            x = symbols('x')
            polinomio_grafica = interpolador.lagrange()
            f_poly = lambdify(x, polinomio_grafica, 'numpy')
            x_continuo = np.linspace(min(x_vals) - 1, max(x_vals) + 1, 200)
            y_continuo = f_poly(x_continuo)
            grafica.ax.plot(x_continuo, y_continuo, label='Polinomio', color='blue', linewidth=2)
            grafica.ax.scatter([x_target], [valor], color='green', s=200,
                             marker='*', label='Punto evaluado', zorder=6, edgecolors='darkgreen', linewidth=1.5)

        grafica.ax.legend(fontsize=10)
        grafica.ax.grid(True, alpha=0.3)
        st.pyplot(grafica.obtener_figura())

    except Exception as e:
        st.error(f"Error: {str(e)}")
