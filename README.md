# Proyecto Api: Sistema de recomendación de peliculas

## índice

1. [Descripción](#descripción)
2. [Lenguaje, bibliotecas y datasets](#lenguaje-bibliotecas-y-datasets)
3. [Proceso de instalación](#proceso-de-instalación)
4. [Carpetas del proyecto](#carpetas-del-proyecto)
5. [Ruta de ejecución de los archivos](#ruta-de-ejecución-de-los-archivos)
6. [Especificaciones de la API](#especificaciones-de-la-api)
7. [Tecnologías utilizadas](#tecnologías-utilizadas)
8. [Contacto](#contacto)


## Descripción

Este es un proyecto, el cual combina conocomimientos tanto de ingeniería de datos y de ciencia de datos. Desde la extracción de datos, su consecuente transformación y carga(ETL) hasta procesos de analalisis exploratorio (y estadístico) de los datos(EDA) y tecnicas de procesamiento de lenguaje natural(NLP)

Esto se hizo mediante el desarrolo de una Api con el framework FastApi desplegadas en la plataforma render, en dicha Api se desarrollaron diferentes endpoints que cumplen inputs para obtener información sobre actores, directores, estrenos de peliculas y principalmente recomendaciones de películas.

El sistema utiliza un modelo de recomendación basad en similitud de contenido, que es capaz de sugerir películas similares a las que un usuario haya visto anteriormente. Esta solución también utiliza técnicas de machine learning para mejorar la experiencia de usuario en plataformas de streaming.

Este proyecto es una muestra de cómo aplicar herramientas modernas de análisis y desarrollo para ofrecer recomendaciones personalizadas, lo que tiene un alto valor práctico en la industria del entretenimiento y las plataformas digitales.

## Lenguaje, bibliotecas y datasets

Lenguaje utilizado: Python 3.11.0

Bibliotecas: Las bibliotecas están especificadas en el archivo requirements.txt

Datasets: [Accede a los datasets aquí](https://drive.google.com/drive/folders/1X_LdCoGTHJDbD28_dJTxaD4fVuQC9Wt5)

## Proceso de instalación:

### 1) Clonar el repositorio:

```bash
   git clone https://github.com/Julianburastero/proyecto_individual-1.git
```

### 2) Crea un entorno virtual para alojar las especifiaddes del proyecto:

```bash
   python -m venv venv
```

### 3) Activa el entorno virtual:
   - En Windows:
     ```bash
     .\venv\Scripts\activate
     ```
   - En Mac/Linux:
     ```bash
     source venv/bin/activate
     ```

### 4) Instala las dependencias necesarias:
   ```bash
   pip install -r requirements.txt
   ```

### Carpetas del proyecto

(Hay diferentes carpetas y archivos la cual se van creando con al consecuente ejecución)

**Proyecto_individual_1**: El archivo cuenta con una carpeta padre que se llama proyecto_individual_1 la cual aloja al resto de carpetas.

**Api**: Esta carpeta contiene el archivo main.py que es donde se crea la api y se desarrollarn los diferentes endpoints

**Data**: Se encuentra la carpeta data la cual contiene todos los datos en crudos directametne alojados en el formato csv

**Data_Post_ETL**: Acá se encuentran todos los datasets procesados y ya disminuidos en tamaño.

**Functions**: Esta carpeta contiene todas las funciones que se irán utilizando a lo largo del desarrollo del proyecto.

**Notebooks**: Acá se encuentran todos los procesos de ETL, el EDA y también la creación del modelo predictorio.

## Ruta de ejecución de los archivos

#### 1) Notebooks/etl_movies.ipynb:

El primer paso es ingresar al archivo recientemente especificado y correr todas las lineas de codigo, en el se hará un proceso de ETL con una gran reducción de filas y columnas ya que se esta trabajando con github y render en su formato gratuito, luego del ETL se enviaran los archivos a una nueva carpeta ya procesados

#### 2) Notebooks/etl_credits.ipynb:

Aca se hace lo mismo que en el anterior paso pero para el archivo credits.csv el cua les bastante más pesado que el anterior y tiene como resutlante dos archivos parquet mucho más livianos.

#### 3) Notebooks/EDA.ipynb:

En este archivo que toca también correr hay diferentes analisis estadisticos de los datos y también hay algunas transformaciones para dejarlo preparado al datasets como modelo predictorio. Este se envia como un modelo a los datos procesados.

### 4) model.ipynb

Aca se debe correr este archivo también el cual contiene la creación del modelo predictorio y se lo envia ya creado con el resto de datos procesados.

### 5) Correr la API

También se puede correr mediante local la aplicación con el siguietne comando:
fastapi dev api/main.py

## Especificaciones de la API

La API ofrece los siguientes endpoints:

- **`/cantidad_filmaciones_mes`**:
  Devuelve el número de películas estrenadas en un mes específico.
  **Parámetro**: `mes` (requerido, en español, ej. "enero").

- **`/puntuacion_titulo`**:
  Devuelve la puntuación de una película.
  **Parámetro**: `titulo` (requerido, nombre de la película).

- **`/votos_titulo`**:
  Devuelve el número de votos y la media de votos de una película.
  **Parámetro**: `titulo` (requerido, nombre de la película).

- **`/obtener_actor`**:
  Devuelve información sobre un actor, como el número de películas y las ganancias generadas.
  **Parámetro**: `actor` (requerido, nombre del actor).

- **`/obtener_director`**:
  Devuelve información sobre un director, como las películas que ha dirigido y el retorno total generado.
  **Parámetro**: `director` (requerido, nombre del director).

- **`/recomendacion/{titulo}`**:
  Devuelve una lista de películas recomendadas basadas en un título específico.
  **Parámetro**: `titulo_pelicula` (requerido, nombre de la película).

## Tecnologías utilizadas

- **fastapi==0.115.4**: Framework para construir la API.

- **ipykernel==6.29.5**: Kernel de Jupyter para ejecutar código Python.

- **ipython==8.29.0**: Entorno interactivo para ejecutar comandos Python.

- **matplotlib==3.9.2**: Biblioteca para la visualización de datos.

- **numpy==2.1.2**: Biblioteca fundamental para cálculos numéricos en Python.

- **pandas==2.2.3**: Manipulación y análisis de datos.

- **pillow==11.0.0**: Biblioteca para la manipulación de imágenes.

- **pyarrow==17.0.0**: Interfaz para Apache Arrow, útil para procesamiento de datos.

- **seaborn==0.13.2**: Biblioteca de visualización de datos basada en Matplotlib.

- **typing_extensions==4.12.2**: Extensiones para el sistema de tipos de Python.

- **tzdata==2024.2**: Base de datos de zonas horarias.

- **uvicorn==0.32.0**: Servidor ASGI para FastAPI.

- **nltk==3.9.1**: Biblioteca para procesamiento de lenguaje natural.

- **scikit-learn==1.5.2**: Herramientas para machine learning, incluida la similitud de contenido.

### Contacto:

## Contacto

- **Correo electrónico**: julianburastero@.com
- **LinkedIn**: [Ir a Linkedin](https://www.linkedin.com/in/julian-burastero-26058320b/)
- **GitHub**: [Ir a Github](https://github.com/Julianburastero)
- **Contribuir al Proyecto**: Si quieres contribuir, abre un Pull Request o abre un Issue [Ir a Github Issues](https://github.com/Julianburastero/proyecto_individual-1/issues).








