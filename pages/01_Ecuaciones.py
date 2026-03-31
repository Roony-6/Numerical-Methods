import streamlit as st
import pandas as pd
from src.metodos import SolucionadorRaices 

def _mostrar_resultado(solver: SolucionadorRaices):
    """Muestra el mensaje de resultado (raíz o error de convergencia)."""
    if solver.convergio:
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"{solver.mensaje}")
        with col2:
            st.metric("Raíz aproximada", f"{solver.raiz:.10f}")
    else:
        st.warning(f"{solver.mensaje}")
        if solver.raiz is not None:
            st.metric("Última aproximación", f"{solver.raiz:.10f}")
            
st.title("Solución de Ecuaciones")
st.write("Usa esta sección para encontrar raíces de funciones no lineales.")

# 1. Inputs del usuario
funcion = st.text_input("Función f(x):", "x**2 - 4")
error_max = st.text_input("Escribe el erro maximo:","1e-6")

metodo = st.selectbox("Selecciona el método:", ["Bisección", "Falsa Posicoin"])

# 2. Lógica 
if st.button("Calcular"):
    solucionador = SolucionadorRaices(funcion) # Instancias tu clase
    if metodo == "Bisección":
        resultado = solucionador.biseccion(0,5)
        _mostrar_resultado(solver=solucionador)
        st.dataframe(pd.DataFrame(resultado))
        
        


