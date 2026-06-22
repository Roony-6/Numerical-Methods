import streamlit as st
from src.metodos.raices import SolucionadorRaices
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo(
    "Solucion de ecuaciones no lineales",
    "Encuentra raices y = 0 usando metodos iterativos"
)

col1, col2 = st.columns([2, 1])
with col1:
    st.subheader("Parametros generales")
with col2:
    st.empty()

col1, col2, col3 = st.columns(3)
with col1:
    funcion = st.text_input("Funcion f(x):", value="x**2 - 4", placeholder="ej: x**2 - 4")
with col2:
    tol = st.number_input("Tolerancia:", value=0.0001, format="%.6f")
with col3:
    max_iter = st.number_input("Iteraciones max:", value=50, step=1)

st.divider()

col1, col2 = st.columns([2, 1])
with col1:
    metodo = st.selectbox(
        "Metodo de solucion:",
        ["Bisección", "Punto Fijo", "Falsa Posicion", "Secante", "Newton Raphson", "Müller"],
        label_visibility="collapsed"
    )
with col2:
    st.empty()

inputs_metodo = InterfaceHelper.inputs_metodo(metodo)

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.empty()
with col2:
    st.empty()
with col3:
    btn_calc = st.button("Calcular", type="primary", use_container_width=True)

if btn_calc:
    solucionador = SolucionadorRaices(funcion, tol=tol, max_iter=max_iter)
    resultado = None

    if metodo == "Bisección":
        raiz, resultado = solucionador.biseccion(inputs_metodo['a'], inputs_metodo['b'])
    elif metodo == "Secante":
        raiz, resultado = solucionador.secante(inputs_metodo['x0'], inputs_metodo['x1'])
    elif metodo == "Punto Fijo":
        raiz, resultado = solucionador.punto_fijo(inputs_metodo['g(x)'], inputs_metodo['p0'])
    elif metodo == "Newton Raphson":
        raiz, resultado = solucionador.newton_rapshon(inputs_metodo['p0'])
    elif metodo == "Falsa Posicion":
        raiz, resultado = solucionador.falsa_posicion(inputs_metodo['a'], inputs_metodo['b'])
    elif metodo == "Müller":
        raiz, resultado = solucionador.muller(inputs_metodo['p0'], inputs_metodo['p1'], inputs_metodo['p2'])

    if resultado is not None:
        st.subheader("Resultados")
        InterfaceHelper.mostrar_metricas(solver=solucionador)

        col_tabla, col_grafica = st.columns(2)

        with col_tabla:
            st.subheader("Historial de iteraciones")
            with st.container():
                if resultado:
                    import pandas as pd
                    df = pd.DataFrame(resultado)
                    df.index += 1
                    st.dataframe(df, use_container_width=True, height=400)

        with col_grafica:
            st.subheader("Grafica")
            grafica = Graficador(titulo=f"Analisis - {metodo}")

            valores_numericos = [v for v in inputs_metodo.values() if isinstance(v, (int, float))]
            rango_a = min(valores_numericos) - 3
            rango_b = max(valores_numericos) + 3
            grafica.graficar_funcion(solucionador.f, rango_a, rango_b)

            puntos_x = [it['aprox'] for it in resultado] if resultado and 'aprox' in resultado[0] else []
            puntos_x = [p.real if isinstance(p, complex) else p for p in puntos_x]
            puntos_y = [solucionador.f(x) for x in puntos_x]
            if puntos_x:
                grafica.marcar_puntos(puntos_x, puntos_y)

            st.pyplot(grafica.obtener_figura())
