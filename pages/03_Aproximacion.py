import streamlit as st
import numpy as np
import pandas as pd
from sympy import symbols, lambdify
from src.metodos.aproximacion import Aproximador
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo("Aproximación de Funciones",
                                  "Ajusta datos con mínimos cuadrados o calcula polinomios de Taylor")

tipo_aproximacion = st.selectbox("Tipo de aproximación:",
                                ["Mínimos Cuadrados Polinomial", "Polinomio de Taylor"])

if tipo_aproximacion == "Mínimos Cuadrados Polinomial":
    st.subheader("📊 Mínimos Cuadrados - Ajuste Polinomial")

    col1, col2 = st.columns([2, 1])
    with col1:
        st.write("**Ingresa los datos (x, y):**")
    with col2:
        n_puntos = st.number_input("Cantidad de puntos:", value=5, min_value=2, max_value=50, label_visibility="collapsed")

    datos_df = pd.DataFrame({
        'x': [float(i) for i in range(n_puntos)],
        'y': [float(i**2) for i in range(n_puntos)]
    })

    datos_editado = st.data_editor(datos_df, num_rows="dynamic", key="datos_aproximacion", use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        grado = st.number_input("Grado del polinomio:", value=2, min_value=1, max_value=10)
    with col2:
        st.empty()
    with col3:
        btn_calc = st.button("🧮 Calcular", type="primary", use_container_width=True)

    if btn_calc:
        try:
            x_vals = datos_editado['x'].values
            y_vals = datos_editado['y'].values

            polinomio, coef, error = Aproximador.minimos_cuadrados(x_vals, y_vals, grado)

            st.success("✓ Ajuste calculado exitosamente")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Error cuadrático", f"{error:.2e}")
            with col2:
                st.metric("Grado del polinomio", grado)

            st.subheader("Polinomio resultante:")
            st.latex(f"P(x) = {polinomio}")

            grafica = Graficador(titulo="Mínimos Cuadrados - Polinomial")
            grafica.ax.scatter(x_vals, y_vals, color='red', s=100, label='Datos', zorder=5)

            x = symbols('x')
            f_poly = lambdify(x, polinomio, 'numpy')
            x_continuo = np.linspace(min(x_vals) - 1, max(x_vals) + 1, 200)
            y_continuo = f_poly(x_continuo)
            grafica.ax.plot(x_continuo, y_continuo, label='Ajuste', color='blue', linewidth=2)

            grafica.ax.legend()
            grafica.ax.grid(True, alpha=0.3)
            st.pyplot(grafica.obtener_figura())

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

else:
    st.subheader("📐 Polinomio de Taylor")

    col1, col2, col3 = st.columns(3)
    with col1:
        funcion = st.text_input("Función f(x):", value="sin(x)", placeholder="ej: sin(x), exp(x), ln(x)")
    with col2:
        x0 = st.number_input("Punto de expansión x₀:", value=0.0)
    with col3:
        grado = st.number_input("Grado n:", value=3, min_value=1, max_value=10)

    btn_taylor = st.button("🧮 Calcular Taylor", type="primary", use_container_width=True)

    if btn_taylor:
        try:
            polinomio_taylor = Aproximador.polinomio_taylor(funcion, x0, grado)

            st.success("✓ Polinomio de Taylor calculado")

            st.subheader("Resultado:")
            st.latex(f"P_{{{grado}}}(x) = {polinomio_taylor}")

            st.info(f"Expandido alrededor de **x₀ = {x0}** con grado **{grado}**")

            grafica = Graficador(titulo=f"Taylor (grado {grado}, x₀={x0})")

            x = symbols('x')
            f_original = lambdify(x, funcion, 'numpy')
            f_taylor = lambdify(x, polinomio_taylor, 'numpy')

            x_continuo = np.linspace(x0 - 5, x0 + 5, 300)
            y_original = f_original(x_continuo)
            y_taylor = f_taylor(x_continuo)

            grafica.ax.plot(x_continuo, y_original, label='f(x) original', color='red', linewidth=2.5)
            grafica.ax.plot(x_continuo, y_taylor, label=f'P_{{{grado}}}(x)', color='blue', linewidth=2.5, linestyle='--')
            grafica.ax.axvline(x=x0, color='green', linestyle=':', alpha=0.6, linewidth=2, label=f'x₀={x0}')
            grafica.ax.scatter([x0], [f_original(x0)], color='green', s=150, zorder=5, edgecolors='darkgreen', linewidth=2)

            grafica.ax.legend(fontsize=10)
            grafica.ax.grid(True, alpha=0.3)
            st.pyplot(grafica.obtener_figura())

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
