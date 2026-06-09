import streamlit as st
import pandas as pd
from src.metodos import SolucionadorRaices 
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo("Solucion de ecuaciones no lineales","Encuentra raices y = 0 usando metodos iterativos")

# 1. Inputs Globales
col1, col2, col3 = st.columns(3)
with col1:
    funcion = st.text_input("Función f(x):", "x**2 - 4")
with col2:
    tol = st.number_input("Tolerancia", value=0.0001, format="%.6f")
with col3:
    max_iter = st.number_input("Iteraciones máx", value=50, step=1)

metodo = st.selectbox("Selecciona el método:", ["Bisección","Punto Fijo", "Falsa Posición", "Secante","Newton Raphson"])

# --- PARÁMETROS ESPECÍFICOS 
inputs_metodo = InterfaceHelper.inputs_metodo(metodo)

# --- BOTÓN DE CÁLCULO ---
if st.button("Calcular"):
    # Instanciamos
    solucionador = SolucionadorRaices(funcion, tol=tol, max_iter=max_iter)
    resultado = None
    
    if metodo == "Bisección":
        raiz, resultado = solucionador.biseccion(inputs_metodo['a'], inputs_metodo['b'])
    elif metodo == "Secante":
        raiz, resultado = solucionador.secante(inputs_metodo['x0'], inputs_metodo['x1'])
    elif metodo == "Punto Fijo":
        raiz,resultado = solucionador.punto_fijo(inputs_metodo['g(x)'],inputs_metodo['a'], inputs_metodo['b'])
    elif metodo == "Newton Raphson":
        raiz,resultado = solucionador.newton_rapshon(inputs_metodo['p0'])
    elif metodo == "Falsa Posición":
        raiz, resultado = solucionador.falsa_posicion(inputs_metodo['a'],inputs_metodo['b'])
    # Mostrar Resultados
    if resultado is not None:
        
        InterfaceHelper.mostrar_metricas(solver=solucionador)
        InterfaceHelper.mostrar_tabla_iteraciones(historial=resultado)
        # Gráfica
        grafica = Graficador(titulo=f"Análisis de {metodo}")
        # Ajustamos el rango de la gráfica según los inputs para que se vea la raíz
        rango_a = min(inputs_metodo.values()) - 3
        rango_b = max(inputs_metodo.values()) + 3
        grafica.graficar_funcion(solucionador.f, rango_a, rango_b)
        
        # Extraemos los puntos x del historial para marcarlos (asumiendo que 'resultado' es una lista de dicts)
        #puntos_x = [it['c'] for it in resultado] if 'c' in resultado[0] else []
        puntos_x = [it['aprox'] for it in resultado] if 'aprox' in resultado[0] else []
        puntos_y = [solucionador.f(x) for x in puntos_x]
        grafica.marcar_puntos(puntos_x, puntos_y)
        
        st.pyplot(grafica.obtener_figura())
        
        #st.write("### Tabla de Iteraciones")
        #st.dataframe(pd.DataFrame(resultado))
        
        
        
