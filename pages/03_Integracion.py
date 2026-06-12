import streamlit as st
from src.metodos.integracion import IntegracionNumerica
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo(
    "Integración Numérica",
    "Aproxima integrales definidas con reglas simples, compuestas y múltiples"
)


def mostrar_resultado(valor, detalles, f=None, a=None, b=None):
    st.success(f"Cálculo completado con {detalles['metodo']}")
    st.metric("Integral aproximada", f"{valor:.10f}")
    with st.expander("Ver detalles del cálculo"):
        st.write(detalles)
    if f is not None:
        graficador = Graficador(f"Área bajo la curva — {detalles['metodo']}")
        figura = graficador.graficar_area_bajo_curva(f, a, b, puntos_x=detalles.get("nodos"))
        st.pyplot(figura)


tab_simple, tab_compuesta, tab_multiple = st.tabs(
    ["Integración Simple", "Integración Compuesta", "Integración Múltiple"]
)

with tab_simple:
    c1, c2, c3 = st.columns(3)
    funcion = c1.text_input("Función f(x):", "x**2", key="f_simple")
    a = c2.number_input("Límite a:", value=0.0, key="a_simple")
    b = c3.number_input("Límite b:", value=2.0, key="b_simple")
    metodo = st.selectbox("Método:", ["Trapecio", "Simpson 1/3", "Simpson 3/8", "Punto Medio"],
                          key="metodo_simple")

    if st.button("Calcular", type="primary", key="btn_simple"):
        try:
            integrador = IntegracionNumerica(funcion)
            if metodo == "Trapecio":
                valor, detalles = integrador.regla_trapecio(a, b)
            elif metodo == "Simpson 1/3":
                valor, detalles = integrador.regla_simpson_1_3(a, b)
            elif metodo == "Simpson 3/8":
                valor, detalles = integrador.regla_simpson_3_8(a, b)
            else:
                valor, detalles = integrador.regla_punto_medio(a, b)
            mostrar_resultado(valor, detalles, integrador.f, a, b)
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab_compuesta:
    c1, c2, c3, c4 = st.columns(4)
    funcion_c = c1.text_input("Función f(x):", "x**2", key="f_comp")
    a_c = c2.number_input("Límite a:", value=0.0, key="a_comp")
    b_c = c3.number_input("Límite b:", value=2.0, key="b_comp")
    n_c = c4.number_input("Subintervalos (n):", value=6, min_value=1, step=1, key="n_comp")
    metodo_c = st.selectbox("Método:", ["Trapecio", "Simpson 1/3", "Simpson 3/8", "Punto Medio"],
                            key="metodo_comp")

    if st.button("Calcular", type="primary", key="btn_comp"):
        try:
            integrador = IntegracionNumerica(funcion_c)
            n_int = int(n_c)
            if metodo_c == "Trapecio":
                valor, detalles = integrador.trapecio_compuesta(a_c, b_c, n_int)
            elif metodo_c == "Simpson 1/3":
                valor, detalles = integrador.simpson_1_3_compuesta(a_c, b_c, n_int)
            elif metodo_c == "Simpson 3/8":
                valor, detalles = integrador.simpson_3_8_compuesta(a_c, b_c, n_int)
            else:
                valor, detalles = integrador.punto_medio_compuesta(a_c, b_c, n_int)
            mostrar_resultado(valor, detalles, integrador.f, a_c, b_c)
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab_multiple:
    metodo_m = st.selectbox("Método:", ["Integral Doble (Simpson 1/3)", "Cuadratura Gaussiana"],
                            key="metodo_mult")

    if metodo_m == "Integral Doble (Simpson 1/3)":
        funcion_xy = st.text_input("Función f(x, y):", "x*y", key="f_doble")
        c1, c2, c3, c4 = st.columns(4)
        a_m = c1.number_input("a (x inicial):", value=0.0, key="a_doble")
        b_m = c2.number_input("b (x final):", value=1.0, key="b_doble")
        c_m = c3.number_input("c (y inicial):", value=0.0, key="c_doble")
        d_m = c4.number_input("d (y final):", value=1.0, key="d_doble")
        c5, c6 = st.columns(2)
        n_m = c5.number_input("n (subintervalos en x, par):", value=10, min_value=2, step=2, key="n_doble")
        m_m = c6.number_input("m (subintervalos en y, par):", value=10, min_value=2, step=2, key="m_doble")

        if st.button("Calcular", type="primary", key="btn_doble"):
            try:
                valor, detalles = IntegracionNumerica.integral_doble_simpson(
                    funcion_xy, a_m, b_m, c_m, d_m, int(n_m), int(m_m)
                )
                mostrar_resultado(valor, detalles)
            except Exception as e:
                st.error(f"Error en el cálculo: {e}")
    else:
        c1, c2, c3, c4 = st.columns(4)
        funcion_g = c1.text_input("Función f(x):", "x**2", key="f_gauss")
        a_g = c2.number_input("Límite a:", value=0.0, key="a_gauss")
        b_g = c3.number_input("Límite b:", value=2.0, key="b_gauss")
        n_g = c4.number_input("Puntos de Gauss:", value=2, min_value=1, max_value=10, step=1, key="n_gauss")

        if st.button("Calcular", type="primary", key="btn_gauss"):
            try:
                integrador = IntegracionNumerica(funcion_g)
                valor, detalles = integrador.integral_gaussiana(a_g, b_g, int(n_g))
                mostrar_resultado(valor, detalles, integrador.f, a_g, b_g)
            except Exception as e:
                st.error(f"Error en el cálculo: {e}")
