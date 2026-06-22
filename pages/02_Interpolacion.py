import streamlit as st
import numpy as np
import pandas as pd
from sympy import symbols, lambdify
from src.metodos.interpolacion import Interpolador
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo("Interpolación Polinomial",
                                  "Interpola datos usando Diferencias Divididas, Lagrange o Neville")

# 1. Entrada de datos
st.subheader("Ingresa los datos (x, y)")

col1, col2 = st.columns(2)
with col1:
    n_puntos = st.number_input("Cantidad de puntos:", value=3, min_value=2, max_value=20)

datos_df = pd.DataFrame({
    'x': [float(i) for i in range(n_puntos)],
    'y': [float(i**2) for i in range(n_puntos)]
})

datos_editado = st.data_editor(datos_df, num_rows="dynamic", key="datos_interpolacion")

# 2. Seleccionar método
metodo = st.selectbox("Selecciona el método:",
                     ["Diferencias Divididas", "Lagrange", "Neville"])

# 3. Inputs específicos del método
x_target = None
if metodo == "Neville":
    x_target = st.number_input("Valor x a interpolar:", value=0.5)

# 4. Botón de cálculo
if st.button("Calcular"):
    try:
        x_vals = datos_editado['x'].values
        y_vals = datos_editado['y'].values

        interpolador = Interpolador(x_vals, y_vals)

        if metodo == "Diferencias Divididas":
            polinomio, tabla = interpolador.diferencias_divididas()
            st.success("✓ Polinomio calculado")
            st.latex(f"P(x) = {polinomio}")
            InterfaceHelper.mostrar_tabla_diferencias(tabla, x_vals)

        elif metodo == "Lagrange":
            polinomio = interpolador.lagrange()
            st.success("✓ Polinomio de Lagrange calculado")
            st.latex(f"P(x) = {polinomio}")

        elif metodo == "Neville":
            valor, matriz = interpolador.neville(x_target)
            st.success("✓ Valor interpolado")
            st.metric("f(x_target) ≈", f"{valor:.10f}")
            with st.expander("Ver matriz de Neville"):
                df_neville = pd.DataFrame(matriz)
                st.dataframe(df_neville, use_container_width=True)

        # Graficar
        grafica = Graficador(titulo=f"Interpolación - {metodo}")

        grafica.ax.scatter(x_vals, y_vals, color='red', s=100, label='Datos', zorder=5)

        if metodo != "Neville":
            x = symbols('x')
            f_poly = lambdify(x, polinomio, 'numpy')
            x_continuo = np.linspace(min(x_vals) - 1, max(x_vals) + 1, 200)
            y_continuo = f_poly(x_continuo)
            grafica.ax.plot(x_continuo, y_continuo, label='Polinomio', color='blue')
        else:
            x = symbols('x')
            polinomio_grafica = interpolador.lagrange()
            f_poly = lambdify(x, polinomio_grafica, 'numpy')
            x_continuo = np.linspace(min(x_vals) - 1, max(x_vals) + 1, 200)
            y_continuo = f_poly(x_continuo)
            grafica.ax.plot(x_continuo, y_continuo, label='Polinomio', color='blue')
            grafica.ax.scatter([x_target], [valor], color='green', s=150,
                             marker='*', label='Punto evaluado', zorder=6)

        grafica.ax.legend()
        grafica.ax.grid(True, alpha=0.3)
        st.pyplot(grafica.obtener_figura())

    except Exception as e:
        st.error(f"Error: {str(e)}")
