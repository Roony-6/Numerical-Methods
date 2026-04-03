import streamlit as st
import pandas as pd

class InterfaceHelper:
    
    # --- Metodos para visuales del main ---
    @staticmethod
    def encabezado_main(nombre, descripcion):
        st.title(nombre)
        st.subheader(descripcion)
        st.markdown("---")
        
    # --- Mostrar inputs parametros especificos para cada metodo
    @staticmethod
    def inputs_metodo(metodo:str):
        inputs_necesarios = {} # Diccionario para guardar los parametros necesarios de cada metodo

        if metodo in ["Bisección", "Punto Fijo","Falsa Posición"]:
            st.write("Define el intervalo [a, b]")
            c1, c2 = st.columns(2)
            inputs_necesarios['a'] = c1.number_input("Valor de a:", value=0.0)
            inputs_necesarios['b'] = c2.number_input("Valor de b:", value=5.0)
            return inputs_necesarios

        elif metodo == "Secante":
            st.write("Define las aproximaciones iniciales")
            c1, c2 = st.columns(2)
            inputs_necesarios['x0'] = c1.number_input("x0:", value=0.0)
            inputs_necesarios['x1'] = c2.number_input("x1:", value=1.0)
            return inputs_necesarios
        
    # --- Metodos para visuales de de los metodos iterativos para encontrar raices ---"
    @staticmethod
    def mostrar_metricas(solver):
        """Muestra los indicadores de éxito, error y la raíz."""
        convergio = getattr(solver, 'convergio', False)
        mensaje = getattr(solver, 'mensaje', "Estado desconocido")
        raiz = getattr(solver, 'raiz', None)

        if convergio:
            st.success(f"{mensaje}")
            if raiz is not None:
                st.metric("Raíz Aproximada", f"{raiz:.10f}")
        else:
            st.warning(f"{mensaje}")
            if raiz is not None:
                st.metric("Última Aproximación", f"{raiz:.10f}", delta="No convergió", delta_color="inverse")

    @staticmethod
    def mostrar_tabla_iteraciones(historial):
        """Convierte la lista de diccionarios en un DataFrame bonito."""
        if historial:
            with st.expander("Ver tabla de iteraciones", expanded=True):
                df = pd.DataFrame(historial)
                # Opcional: poner el índice empezando en 1
                df.index += 1 
                st.dataframe(df, use_container_width=True)

    @staticmethod
    def encabezado_metodo(nombre, descripcion):
        """Genera un título y descripción estandarizada."""
        st.header(f"{nombre}")
        st.caption(descripcion)
        st.divider()
        