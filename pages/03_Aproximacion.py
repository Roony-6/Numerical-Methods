import streamlit as st
import numpy as np
import pandas as pd
from sympy import symbols, lambdify
from src.metodos.aproximacion import Aproximador
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo("Aproximación de Funciones",
                                  "Ajusta datos con mínimos cuadrados o calcula polinomios de Taylor")

tipo_aproximacion = st.selectbox("Selecciona el tipo de aproximación:",
                                ["Mínimos Cuadrados", "Polinomio de Taylor"])

if tipo_aproximacion == "Mínimos Cuadrados":
    st.subheader("Mínimos Cuadrados")

    metodo_mc = st.radio("Elige el tipo de ajuste:", ["Polinomial", "Exponencial"])

    st.write("Ingresa los datos (x, y):")
    col1, col2 = st.columns(2)
    with col1:
        n_puntos = st.number_input("Cantidad de puntos:", value=5, min_value=2, max_value=50)

    datos_df = pd.DataFrame({
        'x': [float(i) for i in range(n_puntos)],
        'y': [float(i**2) for i in range(n_puntos)]
    })

    datos_editado = st.data_editor(datos_df, num_rows="dynamic", key="datos_aproximacion")

    if metodo_mc == "Polinomial":
        grado = st.number_input("Grado del polinomio:", value=2, min_value=1, max_value=10)

        if st.button("Calcular ajuste polinomial"):
            try:
                x_vals = datos_editado['x'].values
                y_vals = datos_editado['y'].values

                polinomio, coef, error = Aproximador.minimos_cuadrados(x_vals, y_vals, grado)

                st.success("✓ Ajuste calculado")
                st.latex(f"P(x) = {polinomio}")
                st.metric("Error cuadrático", f"{error:.10f}")

                grafica = Graficador(titulo="Mínimos Cuadrados - Polinomial")
                grafica.ax.scatter(x_vals, y_vals, color='red', s=100, label='Datos', zorder=5)

                x = symbols('x')
                f_poly = lambdify(x, polinomio, 'numpy')
                x_continuo = np.linspace(min(x_vals) - 1, max(x_vals) + 1, 200)
                y_continuo = f_poly(x_continuo)
                grafica.ax.plot(x_continuo, y_continuo, label='Ajuste', color='blue')

                grafica.ax.legend()
                grafica.ax.grid(True, alpha=0.3)
                st.pyplot(grafica.obtener_figura())

            except Exception as e:
                st.error(f"Error: {str(e)}")

    else:
        if st.button("Calcular ajuste exponencial"):
            try:
                x_vals = datos_editado['x'].values
                y_vals = datos_editado['y'].values

                polinomio, (a, b), error = Aproximador.minimos_cuadrados_exponencial(x_vals, y_vals)

                st.success("✓ Ajuste exponencial calculado")
                st.latex(f"f(x) = {polinomio}")
                col1, col2 = st.columns(2)
                col1.metric("Coeficiente a", f"{a:.6f}")
                col2.metric("Exponente b", f"{b:.6f}")
                st.metric("Error cuadrático", f"{error:.10f}")

                grafica = Graficador(titulo="Mínimos Cuadrados - Exponencial")
                grafica.ax.scatter(x_vals, y_vals, color='red', s=100, label='Datos', zorder=5)

                x = symbols('x')
                f_poly = lambdify(x, polinomio, 'numpy')
                x_continuo = np.linspace(min(x_vals), max(x_vals), 200)
                y_continuo = f_poly(x_continuo)
                grafica.ax.plot(x_continuo, y_continuo, label='Ajuste', color='blue')

                grafica.ax.legend()
                grafica.ax.grid(True, alpha=0.3)
                st.pyplot(grafica.obtener_figura())

            except Exception as e:
                st.error(f"Error: {str(e)}")

else:
    st.subheader("Polinomio de Taylor")

    col1, col2, col3 = st.columns(3)
    with col1:
        funcion = st.text_input("f(x):", "sin(x)")
    with col2:
        x0 = st.number_input("Punto x0:", value=0.0)
    with col3:
        grado = st.number_input("Grado:", value=3, min_value=1, max_value=10)

    if st.button("Calcular polinomio de Taylor"):
        try:
            polinomio_taylor = Aproximador.polinomio_taylor(funcion, x0, grado)

            st.success("✓ Polinomio de Taylor calculado")
            st.latex(f"P_{{\\{grado}}}(x) = {polinomio_taylor}")

            grafica = Graficador(titulo=f"Polinomio de Taylor (grado {grado}, x0={x0})")

            x = symbols('x')
            f_original = lambdify(x, funcion, 'numpy')
            f_taylor = lambdify(x, polinomio_taylor, 'numpy')

            x_continuo = np.linspace(x0 - 5, x0 + 5, 300)
            y_original = f_original(x_continuo)
            y_taylor = f_taylor(x_continuo)

            grafica.ax.plot(x_continuo, y_original, label='f(x) original', color='red', linewidth=2)
            grafica.ax.plot(x_continuo, y_taylor, label=f'P_{{{grado}}}(x)', color='blue', linewidth=2)
            grafica.ax.axvline(x=x0, color='green', linestyle='--', alpha=0.5, label=f'x0={x0}')
            grafica.ax.scatter([x0], [f_original(x0)], color='green', s=100, zorder=5)

            grafica.ax.legend()
            grafica.ax.grid(True, alpha=0.3)
            st.pyplot(grafica.obtener_figura())

        except Exception as e:
            st.error(f"Error: {str(e)}")
