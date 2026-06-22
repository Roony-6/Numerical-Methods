import streamlit as st
from src.metodos.integracion import IntegracionNumerica
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo(
    "Integracion Numerica",
    "Aproxima integrales definidas con reglas simples, compuestas y multiples"
)


def mostrar_resultado(valor, detalles, f=None, a=None, b=None):
    st.success(f"Calculo completado con {detalles['metodo']}")
    st.metric("Integral aproximada", f"{valor:.10f}")
    with st.expander("Ver detalles del calculo"):
        st.write(detalles)
    if f is not None:
        graficador = Graficador(f"Area bajo la curva - {detalles['metodo']}")
        figura = graficador.graficar_area_bajo_curva(f, a, b, puntos_x=detalles.get("nodos"))
        st.pyplot(figura)


tab_simple, tab_compuesta, tab_multiple, tab_avanzado = st.tabs(
    ["Integracion Simple", "Integracion Compuesta", "Integracion Multiple", "Metodos Avanzados"]
)

with tab_simple:
    st.subheader("Parametros")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        funcion = st.text_input("f(x):", value="x**2", key="f_simple")
    with col2:
        a = st.number_input("a:", value=0.0, key="a_simple")
    with col3:
        b = st.number_input("b:", value=2.0, key="b_simple")
    with col4:
        metodo = st.selectbox("Metodo:", ["Trapecio", "Simpson 1/3", "Simpson 3/8"],
                              key="metodo_simple", label_visibility="collapsed")

    if st.button("Calcular", type="primary", key="btn_simple", use_container_width=True):
        try:
            integrador = IntegracionNumerica(funcion)
            if metodo == "Trapecio":
                valor, detalles = integrador.regla_trapecio(a, b)
            elif metodo == "Simpson 1/3":
                valor, detalles = integrador.regla_simpson_1_3(a, b)
            else:
                valor, detalles = integrador.regla_simpson_3_8(a, b)
            mostrar_resultado(valor, detalles, integrador.f, a, b)
        except Exception as e:
            st.error(f"Error en el calculo: {e}")

with tab_compuesta:
    st.subheader("Parametros")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        funcion_c = st.text_input("f(x):", value="x**2", key="f_comp")
    with col2:
        a_c = st.number_input("a:", value=0.0, key="a_comp")
    with col3:
        b_c = st.number_input("b:", value=2.0, key="b_comp")
    with col4:
        n_c = st.number_input("n:", value=6, min_value=1, step=1, key="n_comp")

    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        metodo_c = st.selectbox("Metodo:", ["Trapecio", "Simpson 1/3", "Simpson 3/8"],
                                key="metodo_comp", label_visibility="collapsed")
    with col2:
        st.empty()
    with col3:
        btn_comp = st.button("Calcular", type="primary", key="btn_comp", use_container_width=True)

    if btn_comp:
        try:
            integrador = IntegracionNumerica(funcion_c)
            n_int = int(n_c)
            if metodo_c == "Trapecio":
                valor, detalles = integrador.trapecio_compuesta(a_c, b_c, n_int)
            elif metodo_c == "Simpson 1/3":
                valor, detalles = integrador.simpson_1_3_compuesta(a_c, b_c, n_int)
            else:
                valor, detalles = integrador.simpson_3_8_compuesta(a_c, b_c, n_int)
            mostrar_resultado(valor, detalles, integrador.f, a_c, b_c)
        except Exception as e:
            st.error(f"Error en el calculo: {e}")

with tab_multiple:
    st.subheader("Selecciona el metodo")
    metodo_m = st.selectbox("Metodo:", ["Integral Doble (Simpson 1/3)", "Cuadratura Gaussiana"],
                            key="metodo_mult", label_visibility="collapsed")

    if metodo_m == "Integral Doble (Simpson 1/3)":
        st.subheader("Parametros")
        st.write("Funcion f(x, y):")
        funcion_xy = st.text_input("", value="x*y", key="f_doble", label_visibility="collapsed")

        col1, col2, col3, col4 = st.columns(4)
        with col1:
            a_m = st.number_input("a (x inicial):", value=0.0, key="a_doble")
        with col2:
            b_m = st.number_input("b (x final):", value=1.0, key="b_doble")
        with col3:
            c_m = st.number_input("c (y inicial):", value=0.0, key="c_doble")
        with col4:
            d_m = st.number_input("d (y final):", value=1.0, key="d_doble")

        col1, col2 = st.columns(2)
        with col1:
            n_m = st.number_input("n (subintervalos en x, par):", value=10, min_value=2, step=2, key="n_doble")
        with col2:
            m_m = st.number_input("m (subintervalos en y, par):", value=10, min_value=2, step=2, key="m_doble")

        if st.button("Calcular", type="primary", key="btn_doble", use_container_width=True):
            try:
                valor, detalles = IntegracionNumerica.integral_doble_simpson(
                    funcion_xy, a_m, b_m, c_m, d_m, int(n_m), int(m_m)
                )
                mostrar_resultado(valor, detalles)
            except Exception as e:
                st.error(f"Error en el calculo: {e}")

    else:
        st.subheader("Parametros")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            funcion_g = st.text_input("f(x):", value="x**2", key="f_gauss")
        with col2:
            a_g = st.number_input("a:", value=0.0, key="a_gauss")
        with col3:
            b_g = st.number_input("b:", value=2.0, key="b_gauss")
        with col4:
            n_g = st.number_input("Puntos:", value=2, min_value=1, max_value=10, step=1, key="n_gauss")

        if st.button("Calcular", type="primary", key="btn_gauss", use_container_width=True):
            try:
                integrador = IntegracionNumerica(funcion_g)
                valor, detalles = integrador.integral_gaussiana(a_g, b_g, int(n_g))
                mostrar_resultado(valor, detalles, integrador.f, a_g, b_g)
            except Exception as e:
                st.error(f"Error: {e}")

with tab_avanzado:
    st.subheader("Selecciona el metodo")
    metodo_a = st.selectbox("Metodo avanzado:", ["Gauss-Legendre", "Adaptativa"],
                            key="metodo_avanzado", label_visibility="collapsed")

    if metodo_a == "Gauss-Legendre":
        st.subheader("Parametros")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            funcion_a = st.text_input("f(x):", value="x**2", key="f_gauss_leg")
        with col2:
            a_a = st.number_input("a:", value=0.0, key="a_gauss_leg")
        with col3:
            b_a = st.number_input("b:", value=2.0, key="b_gauss_leg")
        with col4:
            n_a = st.number_input("Puntos:", value=3, min_value=1, max_value=20, key="n_gauss_leg")

        if st.button("Calcular", type="primary", key="btn_gauss_leg", use_container_width=True):
            try:
                integrador = IntegracionNumerica(funcion_a)
                valor, detalles = integrador.cuadratura_gauss_legendre(a_a, b_a, int(n_a))
                mostrar_resultado(valor, detalles, integrador.f, a_a, b_a)
            except Exception as e:
                st.error(f"Error: {e}")

    else:
        st.subheader("Parametros")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            funcion_ad = st.text_input("f(x):", value="x**2", key="f_adapt")
        with col2:
            a_ad = st.number_input("a:", value=0.0, key="a_adapt")
        with col3:
            b_ad = st.number_input("b:", value=2.0, key="b_adapt")
        with col4:
            tol_ad = st.number_input("Tolerancia:", value=1e-6, format="%.2e", key="tol_adapt")

        if st.button("Calcular", type="primary", key="btn_adapt", use_container_width=True):
            try:
                integrador = IntegracionNumerica(funcion_ad)
                valor, detalles = integrador.cuadratura_adaptativa(a_ad, b_ad, tol_ad)
                st.success(f"Calculo completado con {detalles['metodo']}")
                st.metric("Integral aproximada", f"{valor:.10f}")
                col1, col2 = st.columns(2)
                col1.metric("Tolerancia", f"{detalles['tolerancia']:.2e}")
                col2.metric("Puntos evaluados", len(detalles['nodos']))
                with st.expander("Ver detalles del calculo"):
                    st.write(detalles)
                graficador = Graficador(f"Area bajo la curva - {detalles['metodo']}")
                figura = graficador.graficar_area_bajo_curva(integrador.f, a_ad, b_ad, puntos_x=detalles.get("nodos"))
                st.pyplot(figura)
            except Exception as e:
                st.error(f"Error: {e}")
