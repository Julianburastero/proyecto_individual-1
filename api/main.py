# Importamos las librerias:
from fastapi import FastAPI
import pandas as pd
import joblib
import os
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

# Leemos los archivos:
movies_df = pd.read_parquet('data_post_etl/movies/movies_dataset_etl.parquet')
cast = pd.read_parquet('data_post_etl/credits/cast_transformados.parquet')
crew = pd.read_parquet('data_post_etl/credits/crew_transformados.parquet')
modelo_prediccion = pd.read_parquet('data_post_etl/prediccion/modelo_prediccion.parquet')
matriz = joblib.load(os.path.join('data_post_etl/prediccion', 'matriz.pkl'))
matriz_reducida = joblib.load(os.path.join('data_post_etl/prediccion', 'matriz_reducida.pkl'))

# Creamos la aplicación:
app = FastAPI()

# Creamos una lista con todos los meses del año:
meses = {
            'enero': 1, 'febrero': 2, 'marzo':3, 'abril':4, 'mayo': 5, 'junio':6, 'julio':7, 
            'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre': 11, 'diciembre': 12
}

# Creamos una lista con todos los días del año:
dias = {
    'lunes':0, 'martes':1, 'miercoles':2, 'jueves':3, 'viernes':4, 'sabado':5, 'domingo':6
}

# Ejecutamos una prueba de la aplicación imprimiento un hola mundo:
@app.get("/")
def read_root():
    return {"Hola": "Mundo"}

# Este endopoint se encarga de devolver todas las peliculas estrenadas en el mes que diga el input
@app.get("/cantidad_filmaciones_mes")
async def cantidad_filmaciones_mes(mes: str) -> dict:

    # Limpiamos y convertimos el mes a minúsculas:
    mes = mes.strip().lower()

    # Verificamos si el mes ingresado es válido (solo letras y un mes en español existente):
    if not mes.isalpha() or mes not in meses:
        return {"error": "Por favor, ingresa un mes en español válido."}

    # Asignamos el número correspondiente al mes:
    mes_numero = meses[mes]

    # Filtramos las películas por el mes correspondiente en la fecha de estreno:
    cantidad_filmaciones = movies_df[movies_df['release_date'].dt.month == mes_numero]
    
    # Verificamos si no hay películas para el mes especificado:
    if cantidad_filmaciones.empty:
        return {"message": f"No hay filmaciones para el mes de {mes}."}
        
    # Calculamos la cantidad de películas para el mes especificado:
    cantidad_filmaciones = len(cantidad_filmaciones)

    # Devolvemos el mensaje con la cantidad de películas estrenadas en ese mes:
    return {"Mensaje de salida": f"{cantidad_filmaciones} películas fueron estrenadas en los meses de {mes.capitalize()}"}

# Este endopoint se encarga de devolver todas las peliculas estrenadas en el dia de la semana que diga el input
@app.get("/cantidad_filmaciones_dia")
async def cantidad_filmaciones_dia(dia: str) -> dict:

    # Verificamos si el día ingresado es válido y está en español:
    if not dia.isalpha() or dia not in dias:
        return {"error": "Por favor, ingresa un día en español válido."}

    # Limpiamos y convertimos el día a minúsculas:
    dia = dia.strip().lower()

    # Obtenemos el número correspondiente al día de la semana:
    dia_numero = dias[dia]

    # Filtramos las películas que fueron estrenadas en el día específico:
    cantidad_filmaciones_dia = movies_df[movies_df['release_date'].dt.dayofweek == dia_numero]

    # Verificamos si no hay películas para ese día:
    if cantidad_filmaciones_dia.empty:
        return {"message": f"No hay filmaciones para el día {dia.capitalize()}."}

    # Calculamos la cantidad de películas estrenadas en ese día:
    cantidad_filmaciones_dia = len(cantidad_filmaciones_dia)

    # Devolvemos el mensaje con la cantidad de películas estrenadas en el día especificado:
    return {'Mensaje de salida': f'La cantidad de filmaciones que se estrenaron en el dia {dia.capitalize()} es de {cantidad_filmaciones_dia} películas'}

# Este endpoint se encarga de devolver el año que se estrenó el titulo del imput junto con la popularidad que obtuvo
@app.get("/puntuacion_titulo")
async def puntuacion_titulo(titulo: str) -> dict:

    # Limpiamos el título, lo convertimos a minúsculas y eliminamos espacios al principio y al final:
    pelicula = titulo.lower().strip()

    # Verificamos si el título está vacío:
    if not pelicula:
        return {"error": "Has ingresado una cadena vacía. Por favor ingresa un título válido."}

    # Verificamos que el título solo contenga caracteres alfanuméricos y espacios:
    if not all(caracter.isalnum() or caracter.isspace() for caracter in pelicula):
        return {"error": "Por favor ingresa un título sin símbolos."}

    # Verificamos si la película existe en la base de datos:
    if pelicula not in movies_df['title'].values:
        return {"error": f"La película {titulo.capitalize()} no existe o no se encuentra dentro de la base de datos."}

    # Obtenemos los datos de la película:
    datos_pelicula = movies_df.loc[movies_df['title'] == pelicula]

    # Obtenemos el año de estreno y la popularidad de la película:
    año = datos_pelicula['release_year'].iloc[0]
    popularidad = datos_pelicula['popularity'].iloc[0]

    # Devolvemos el mensaje con la información solicitada:
    return {"Mensaje de salida": f"La película {pelicula.capitalize()} fue estrenada el año {año} y obtuvo un score de {popularidad}"}

# Este endpoint se encarga de entregar la cantidad total de votos y su media:
@app.get("/votos_titulo")
async def votos_titulo(titulo: str) -> dict:

    # Limpiamos y convertimos el título a minúsculas:
    pelicula = titulo.lower().strip()

    # Verificamos si el título está vacío:
    if not pelicula:
        return {"error": "Has ingresado una cadena vacía. Por favor ingresa un título válido."}

    # Comprobamos que solo contenga caracteres alfanuméricos y espacios:
    if not all(caracter.isalnum() or caracter.isspace() for caracter in pelicula):
        return {"error": "Por favor ingresa un título sin símbolos."}

    # Comprobamos si la película existe en la base de datos:
    if pelicula not in movies_df['title'].values:
        return {"error": f"La película {titulo.capitalize()} no existe o no se encuentra dentro de la base de datos."}

    # Obtiene los datos de la película
    datos_pelicula = movies_df.loc[movies_df['title'] == pelicula]

    # Comprobamos los votos de la película:
    if not datos_pelicula.empty:
        cantidad_votos = datos_pelicula['vote_count'].iloc[0]

    # Verificamos si la cantidad de votos es suficiente:
    if cantidad_votos < 2000:
            return {"error": f"La película {titulo.capitalize()} tiene muy pocas votaciones para ser considerada."}
    
    # Obtenemos la media de los votos:
    media_votos = datos_pelicula['vote_average'].iloc[0]

    # Devolvemos los resultados:
    return {"Mensaje de salida": f"La película {pelicula.capitalize()} tiene un total de {cantidad_votos} y una media de valoración de {media_votos}"}

# Este endpoint se encarga de entregar la cantidad de peliculas en las que participo el actor junto con el total de sus ganancias:
@app.get('/obtener_actor')
async def obtener_actor(actor: str) -> dict:

    # Limpiamos y convertimos el nombre del actor a minúsculas:
    actor = actor.lower().strip()

    # Verificamos si el nombre está vacío:
    if not actor:
        return {"error": "Has ingresado una cadena vacía. Por favor ingresa un nombre  y apellido de actor válido."}

    # Comprobamos que solo contiene letras y espacios:
    if not all(char.isalpha() or char.isspace() for char in actor):
        raise HTTPException(status_code=400, detail="El nombre del actor debe contener solo letras y/o espacios.")

    # Verificamos si el actor está en la base de datos:
    if actor not in cast['name'].values:
        return {"error": f"El nombre {actor.capitalize()} no es un actor o no se encuentra dentro de la base de datos."}

    # Obtenemos las películas del actor:
    ids_peliculas_actor = cast.loc[cast['name'] == actor]['id_credits'].unique()

    # Calculamos la cantidad de películas y las ganancias:
    cantidad_peliculas = len(ids_peliculas_actor)
    ganancia = round(movies_df[movies_df['id'].isin(ids_peliculas_actor)]['return'].sum(), 2)
    promedio_ganancia = round(movies_df[movies_df['id'].isin(ids_peliculas_actor)]['return'].mean(), 2)

    # Devolvemos la información:
    return {"Mensaje de salida": f"El actor {actor.capitalize()} ha participado en {cantidad_peliculas} películas, el mismo ha conseguido un retorno de {ganancia} con un promedio de {promedio_ganancia} por filmación"}

# Este endpoint se encarga de entregar el retorno total junto con tas las peliculas que dirigió:
@app.get('/obtener_director')
async def obtener_director(director: str) -> dict:

    # Limpiamos y convertimos el nombre del director a minúsculas:
    director = director.lower().strip()

    # Verificamos si el nombre está vacío:
    if not director:
        return {"Error": "Has ingresado una cadena vacía. Por favor ingresa un nombre y apellido de director válido."}

    # Comprobamos que solo contiene letras y espacios:
    if not all(char.isalpha() or char.isspace() for char in director):
        raise HTTPException(status_code=400, detail="El nombre del director debe contener solo letras y/o espacios.")

    # Verificamos si el director está en la base de datos:
    if director not in crew['name'].str.lower().values:
        return {"error": f"El nombre {director.capitalize()} no es un director o no se encuentra dentro de la base de datos."}

    # Obtenemos las películas del director:
    ids_director = crew.loc[crew['name'].str.lower() == director, 'id_credits'].unique()

    # Filtramos las películas y seleccionamos las columnas de interés:
    peliculas_df = movies_df[movies_df['id'].isin(ids_director)]
    peliculas = peliculas_df[['title', 'release_year', 'budget', 'revenue', 'return']].rename(
        columns={
            'title': 'Titulo',
            'release_year': 'Fecha de estreno',
            'budget': 'Costo',
            'revenue': 'Ganancia',
            'return': 'Retorno'
        }
    ).to_dict(orient='records')

    # Calcula el retorno total
    retorno_total = round(peliculas_df['return'].sum(), 2)

    # Devolvemos la información del director y sus películas:
    return {
        "Nombre Director": director,
        "Retorno Total": retorno_total,
        "Peliculas": peliculas
    }

# Este endpoint se encarga de entregar 5 peliculas recomendadas a partir de la pelicula ingresada en el input
@app.get('/recomendacion/{titulo}')
async def recomendar_pelicula(titulo_pelicula: str) ->dict:

    # Buscamos el índice de la película en el modelo:
    indice = modelo_prediccion.index[modelo_prediccion['title'].str.lower() == titulo_pelicula.lower()].tolist()

    # Verificamos si encontramos la película:    
    if not indice:
        return {"Error": "Película no encontrada"}

    # Calculamos la similitud coseno:
    puntajes_similitud = cosine_similarity(matriz_reducida[indice[0]].reshape(1, -1), matriz_reducida)

    # Ordenamos las películas por puntaje de similitud:
    puntajes_similitud = sorted(enumerate(puntajes_similitud[0]), key=lambda x: x[1], reverse=True)

    # Obtenemos las 5 películas más similares:
    indices_peliculas = [i[0] for i in puntajes_similitud[1:6]]
    recomendaciones = modelo_prediccion['title'].iloc[indices_peliculas].tolist()

    # Devolvemos las recomendaciones:
    return {"Peliculas recdomendadas": recomendaciones}
