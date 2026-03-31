# Proyecto de la materia de Metodos Numericos

Este proyecto es una aplicación interactiva diseñada para resolver problemas clásicos de análisis numérico como encontrar raices (por ahora).

---

##  Características Principales

* **Interfaz :** Desarrollada con [Streamlit](https://streamlit.io/), eliminando la necesidad de HTML/CSS manual.
* **Arquitectura :** Implementación de algoritmos mediante clases especializadas
* **Visualización Dinámica:** Gráficas interactivas para analizar el comportamiento de las funciones y la convergencia de los métodos.
<!--* **Soporte LaTeX:** Visualización de fórmulas matemáticas profesionales.-->

---

## Estructura del Proyecto


```text
metodos_numericos/
├── app.py                 #Portada y configuracoin principal
├── pages                  #Interfaz de usuario (Modulos de la App)
│   └── 01_Ecuaciones.py   #Paginas de metodos numericos
├── README.md              #Documentacion (este archivo)
├── requirements.txt       #Dependencias del proyecto
└── src                    #Logica
    ├── __init__.py 
    └── metodos.py         #Clases y metodos de metodos numericos
```

##  Instalación y Ejecución

Sigue estos pasos para configurar el entorno y correr la aplicación en **Linux**.

### 1. Requisitos Previos
Asegúrate de tener instalado Python y el gestor de entornos virtuales:
```bash
sudo pacman -S python python-pip
```
### 2. Configuración del Proyecto

Clona este repositorio (o sitúate en la carpeta del proyecto) y crea un entorno virtual para aislar las dependencias:
```bash
# Crear el entorno virtual
python -m venv .venv
```

### 3. Instalación de Dependencias

Una vez activado el entorno (verás ```.venv``` en tu terminal), instala las librerías necesarias:
```bash
pip install -r requirements.txt
```
### 4. Ejecucion (en local)
Para correr en local la aplicacion corre el siguiente comando:

```bash
streamlit run app.py
```