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

        if metodo in ["Bisección", "Falsa Posición", "Falsa Posicion"]:
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
        elif metodo == "Punto Fijo":
            st.write("Proporciona la función de iteración g(x) y el punto inicial")
            c1, c2 = st.columns(2)
            inputs_necesarios['g(x)'] = c1.text_input("Funcion g(x):", "(x + 4/x) / 2")
            inputs_necesarios['p0'] = c2.number_input("p0:", value=1.0)
            return inputs_necesarios
        elif metodo == "Newton Raphson":
            c1,c2 = st.columns(2)
            inputs_necesarios['p0'] = c1.number_input("p0:", value=0.0)
            return inputs_necesarios
        elif metodo == "Müller":
            st.write("Define las tres aproximaciones iniciales")
            c1, c2, c3 = st.columns(3)
            inputs_necesarios['p0'] = c1.number_input("p0:", value=0.0)
            inputs_necesarios['p1'] = c2.number_input("p1:", value=1.0)
            inputs_necesarios['p2'] = c3.number_input("p2:", value=2.0)
            return inputs_necesarios
        elif metodo == "Neville":
            c1 = st.columns(1)[0]
            inputs_necesarios['x_target'] = c1.number_input("Valor x a interpolar:", value=0.5)
            return inputs_necesarios
        elif metodo == "Mínimos Cuadrados":
            c1, c2 = st.columns(2)
            inputs_necesarios['grado'] = c1.number_input("Grado del polinomio:", value=2, min_value=1, max_value=10)
            return inputs_necesarios
        elif metodo == "Taylor":
            c1, c2, c3 = st.columns(3)
            inputs_necesarios['funcion'] = c1.text_input("f(x):", "sin(x)")
            inputs_necesarios['x0'] = c2.number_input("Punto x0:", value=0.0)
            inputs_necesarios['grado'] = c3.number_input("Grado:", value=3, min_value=1, max_value=10)
            return inputs_necesarios
        elif metodo == "Gauss-Legendre":
            c1, c2, c3 = st.columns(3)
            inputs_necesarios['a'] = c1.number_input("Límite a:", value=0.0)
            inputs_necesarios['b'] = c2.number_input("Límite b:", value=1.0)
            inputs_necesarios['n_puntos'] = c3.number_input("Puntos de Gauss:", value=3, min_value=1, max_value=20)
            return inputs_necesarios
        elif metodo == "Adaptativa":
            c1, c2, c3 = st.columns(3)
            inputs_necesarios['a'] = c1.number_input("Límite a:", value=0.0)
            inputs_necesarios['b'] = c2.number_input("Límite b:", value=1.0)
            inputs_necesarios['tol'] = c3.number_input("Tolerancia:", value=1e-6, format="%.2e")
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

    @staticmethod
    def mostrar_tabla_diferencias(tabla, x_values):
        """Muestra la tabla de diferencias divididas de forma legible."""
        if tabla is not None:
            with st.expander("Ver tabla de diferencias divididas", expanded=True):
                df_display = pd.DataFrame(tabla)
                st.dataframe(df_display, use_container_width=True)
        