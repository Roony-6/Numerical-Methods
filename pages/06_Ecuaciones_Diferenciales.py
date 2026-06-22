import streamlit as st
from src.metodos.edo import SolucionadorEDO, SolucionadorSistemasEDO
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo(
    "Ecuaciones Diferenciales Ordinarias",
    "Resuelve problemas de valor inicial y' = f(x, y) con métodos de un paso, multipaso y sistemas"
)


def inputs_pvi(sufijo):
    c1, c2, c3, c4 = st.columns(4)
    funcion = c1.text_input("Función f(x, y):", "x + y", key=f"f_{sufijo}")
    x0 = c2.number_input("x0 (x inicial):", value=0.0, key=f"x0_{sufijo}")
    y0 = c3.number_input("y0 (y inicial):", value=1.0, key=f"y0_{sufijo}")
    xf = c4.number_input("xf (x final):", value=2.0, key=f"xf_{sufijo}")
    return funcion, x0, y0, xf


def mostrar_resultados(df_resultados, metodo, xf, graficar):
    st.success(f"Cálculo completado con {metodo}")
    m1, m2 = st.columns(2)
    m1.metric(f"y({xf})", f"{df_resultados['y_aprox'].iloc[-1]:.10f}")
    m2.metric("Pasos realizados", len(df_resultados) - 1)

    st.subheader("Tabla de resultados")
    st.dataframe(df_resultados, use_container_width=True)

    graficador = Graficador()
    figura = graficar(graficador, df_resultados)
    st.pyplot(figura)


tab_pvi, tab_heun, tab_sistemas = st.tabs(
    ["Valor Inicial (1er Orden)", "Heun", "Sistemas y Orden Superior"]
)

with tab_pvi:
    funcion, x0, y0, xf = inputs_pvi("pvi")
    metodo = st.selectbox("Método:", ["Euler", "Taylor (Orden 2)", "RK4", "RKF45"],
                          key="metodo_pvi")

    if metodo == "RKF45":
        c5, c6, c7 = st.columns(3)
        tol = c5.number_input("Tolerancia:", value=1e-5, format="%.2e",
                              min_value=1e-12, key="tol_pvi")
        h_min = c6.number_input("h mínimo:", value=0.01, format="%.4f",
                                min_value=1e-6, key="hmin_pvi")
        h_max = c7.number_input("h máximo:", value=0.5, format="%.4f",
                                min_value=1e-6, key="hmax_pvi")
    else:
        h = st.number_input("Tamaño de paso h:", value=0.1, format="%.4f",
                            min_value=1e-6, key="h_pvi")

    if st.button("Calcular", type="primary", key="btn_pvi"):
        try:
            if xf <= x0:
                st.error("El valor final xf debe ser mayor que x0.")
            else:
                solucionador = SolucionadorEDO(funcion)
                if metodo == "Euler":
                    df_resultados = solucionador.metodo_euler(x0, y0, xf, h)
                elif metodo == "Taylor (Orden 2)":
                    df_resultados = solucionador.metodo_taylor_orden_2(x0, y0, xf, h)
                elif metodo == "RK4":
                    df_resultados = solucionador.runge_kutta_4(x0, y0, xf, h)
                else:
                    if h_min > h_max:
                        st.error("h mínimo no puede ser mayor que h máximo.")
                        st.stop()
                    df_resultados = solucionador.runge_kutta_fehlberg(
                        x0, y0, xf, tol, h_min, h_max)

                mostrar_resultados(
                    df_resultados, metodo, xf,
                    lambda g, df: g.graficar_edo(df, f"Aproximación de EDO — {metodo}"))
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab_heun:
    funcion_h, x0_h, y0_h, xf_h = inputs_pvi("heun")
    h_h = st.number_input("Tamaño de paso h:", value=0.1, format="%.4f",
                          min_value=1e-6, key="h_heun")
    st.caption("Metodo predictor-corrector que mejora sobre Euler usando dos evaluaciones de la funcion.")

    if st.button("Calcular", type="primary", key="btn_heun"):
        try:
            if xf_h <= x0_h:
                st.error("El valor final xf debe ser mayor que x0.")
            else:
                solucionador = SolucionadorEDO(funcion_h)
                df_resultados = solucionador.metodo_heun(x0_h, y0_h, xf_h, h_h)
                mostrar_resultados(
                    df_resultados, "Heun", xf_h,
                    lambda g, df: g.graficar_edo(
                        df, "Aproximacion de EDO — Heun"))
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")

with tab_sistemas:
    st.caption("Sistema de la forma y1' = f1(x, y1, ..., yn), ..., yn' = fn(x, y1, ..., yn). "
               "Una EDO de orden superior se reduce a un sistema con yk = y^(k-1).")
    n = st.number_input("Número de ecuaciones (n):", value=2, min_value=1,
                        max_value=6, step=1, key="n_sist")
    n = int(n)

    funciones = []
    condiciones = []
    for i in range(1, n + 1):
        c1, c2 = st.columns([3, 1])
        default_f = "y2" if (i == 1 and n > 1) else ("-y1" if i == n and n > 1 else "x + y1")
        funciones.append(c1.text_input(f"f{i}(x, y1...y{n}):", default_f, key=f"f{i}_sist"))
        condiciones.append(c2.number_input(f"y{i}(x0):", value=1.0 if i == 1 else 0.0,
                                           key=f"y{i}0_sist"))

    c1, c2, c3 = st.columns(3)
    x0_s = c1.number_input("x0 (x inicial):", value=0.0, key="x0_sist")
    xf_s = c2.number_input("xf (x final):", value=2.0, key="xf_sist")
    h_s = c3.number_input("Tamaño de paso h:", value=0.1, format="%.4f",
                          min_value=1e-6, key="h_sist")

    if st.button("Calcular", type="primary", key="btn_sist"):
        try:
            if xf_s <= x0_s:
                st.error("El valor final xf debe ser mayor que x0.")
            else:
                solucionador = SolucionadorSistemasEDO(funciones)
                df_resultados = solucionador.runge_kutta_4_sistemas(
                    x0_s, condiciones, xf_s, h_s)

                st.success("Cálculo completado con RK4 para sistemas")
                metricas = st.columns(n + 1)
                for i, col in enumerate(solucionador.columnas_y):
                    metricas[i].metric(f"{col}({xf_s})",
                                       f"{df_resultados[col].iloc[-1]:.10f}")
                metricas[n].metric("Pasos realizados", len(df_resultados) - 1)

                st.subheader("Tabla de resultados")
                st.dataframe(df_resultados, use_container_width=True)

                graficador = Graficador()
                figura = graficador.graficar_sistema_edo(
                    df_resultados, "Sistema de EDO — RK4")
                st.pyplot(figura)
        except Exception as e:
            st.error(f"Error en el cálculo: {e}")
