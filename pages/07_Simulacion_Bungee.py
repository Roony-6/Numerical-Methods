import time

import streamlit as st
from src.metodos.bungee import SimuladorBungee
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo(
    "Simulación de Salto Bungee",
    "Modelo de caída con cuerda elástica resuelto con RK4: y'' = g - (c/m)y' - (k/m)max(0, y - L)"
)

with st.sidebar:
    st.subheader("Parámetros físicos")
    m = st.slider("Masa del saltador m (kg):", 40.0, 120.0, 70.0, 1.0)
    k = st.slider("Constante elástica k (N/m):", 5.0, 100.0, 30.0, 1.0)
    c = st.slider("Fricción del aire c (kg/s):", 0.0, 30.0, 5.0, 0.5)
    L = st.slider("Longitud de la cuerda L (m):", 5.0, 40.0, 20.0, 1.0)
    t_final = st.slider("Duración de la simulación (s):", 5.0, 30.0, 15.0, 1.0)

if st.button("▶ Iniciar Simulación Bungee", type="primary"):
    dt = 0.02
    simulador = SimuladorBungee()
    df_trayectoria = simulador.calcular_trayectoria(m, k, c, L, t_final, dt)

    y_max_caida = df_trayectoria['y'].max()
    max_y = max(y_max_caida * 1.1, L + 10)

    c1, c2, c3 = st.columns(3)
    c1.metric("Caída máxima", f"{y_max_caida:.2f} m")
    c2.metric("Estiramiento máximo", f"{max(0.0, y_max_caida - L):.2f} m")
    c3.metric("Posición de equilibrio", f"{L + m * simulador.G / k:.2f} m")

    animacion_placeholder = st.empty()
    graficador = Graficador()

    # 1 de cada 5 frames para mantener la animación fluida
    for y_pos in df_trayectoria['y'].iloc[::5]:
        figura = graficador.dibujar_frame_bungee(y_pos, L, max_y)
        animacion_placeholder.pyplot(figura)
        time.sleep(0.02)

    st.subheader("Trayectoria completa")
    st.line_chart(df_trayectoria.set_index('t')['y'] * -1, x_label="t (s)",
                  y_label="posición (m)")
