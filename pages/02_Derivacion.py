import streamlit as st
import pandas as pd
from src.metodos.raices import SolucionadorRaices 
from src.graficador import Graficador
from src.interface import InterfaceHelper

InterfaceHelper.encabezado_metodo("Aproximacion de Derivadas en n puntos","Aproxima derivadas")
#1. Inputs Globales
col1, col2, col3, col4= st.columns(4)
with col1:
    
    funcion = st.text_input("Función f(x):", "x**2 - 4")
with col2:
    tol = st.number_input("Tolerancia", value=0.0001, format="%.6f")
with col3:
    max_iter = st.number_input("Iteraciones máx", value=50, step=1)
with col4:
    a = st.number_input("a: ",value = 0)

