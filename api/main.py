from fastapi import FastAPI
import pandas as pd
import joblib
import os


from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD

# estructurar el message como está en el ejemplo

movies_df = pd.read_parquet('data_post_etl/movies/movies_dataset_etl.parquet')
cast = pd.read_parquet('data_post_etl/credits/cast_transformados.parquet')
crew = pd.read_parquet('data_post_etl/credits/crew_transformados.parquet')

modelo_prediccion = pd.read_parquet('data_post_etl/prediccion/modelo_prediccion.parquet')
matriz = joblib.load(os.path.join('data_post_etl/prediccion', 'matriz.pkl'))
matriz_reducida = joblib.load(os.path.join('data_post_etl/prediccion', 'matriz_reducida.pkl'))

app = FastAPI()

meses = {
            'enero': 1, 'febrero': 2, 'marzo':3, 'abril':4, 'mayo': 5, 'junio':6, 'julio':7, 
            'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre': 11, 'diciembre': 12
}

dias = {
    'lunes':0, 'martes':1, 'miercoles':2, 'jueves':3, 'viernes':4, 'sabado':5, 'domingo':6
}

@app.get("/")
def read_root():
    return {"Hola": "Mundo"}

@app.get("/cantidad_filmaciones_mes")
async def cantidad_filmaciones_mes(mes: str) -> dict:
    
    if not mes.isalpha() or mes not in meses:
        return {"error": "Por favor, ingresa un mes en español válido."}
    
    mes = mes.strip().lower()

    mes_numero = meses[mes]

    cantidad_filmaciones = movies_df[movies_df['release_date'].dt.month == mes_numero]
    
    if cantidad_filmaciones.empty:
        return {"message": f"No hay filmaciones para el mes de {mes}."}
    
    cantidad_filmaciones = len(cantidad_filmaciones)

    return {"Mensaje de salida": f"{cantidad_filmaciones} películas fueron estrenadas en los meses de {mes.capitalize()}"}



#devuelve un dic e nrealidad? ver eso
@app.get("/cantidad_filmaciones_dia")
async def cantidad_filmaciones_dia(dia: str) -> dict:

    if not dia.isalpha() or dia not in dias:
        return {"error": "Por favor, ingresa un día en español válido."}

    dia = dia.strip().lower()

    dia_numero = dias[dia]

    cantidad_filmaciones_dia = movies_df[movies_df['release_date'].dt.dayofweek == dia_numero]

    if cantidad_filmaciones_dia.empty:
        return {"message": f"No hay filmaciones para el día {dia.capitalize()}."}

    cantidad_filmaciones_dia = len(cantidad_filmaciones_dia)

    return {'Mensaje de salida': f'La cantidad de filmaciones que se estrenaron en el dia {dia.capitalize()} es de {cantidad_filmaciones_dia} películas'}
#cambiar el nombre del decorador


@app.get("/titulo_de")
async def puntuacion_titulo(titulo: str) -> dict:

    pelicula = titulo.lower().strip()

    if not pelicula:  # Verifica si la cadena está vacía
        return {"error": "Has ingresado una cadena vacía. Por favor ingresa un título válido."}

    if not all(caracter.isalnum() or caracter.isspace() for caracter in pelicula):
        return {"error": "Por favor ingresa un título sin símbolos."}

    if pelicula not in movies_df['title'].values:
        return {"error": f"La película {titulo.capitalize()} no existe o no se encuentra dentro de la base de datos."}

    datos_pelicula = movies_df.loc[movies_df['title'] == pelicula]
    año = datos_pelicula['release_year'].iloc[0]
    popularidad = datos_pelicula['popularity'].iloc[0]

    return {"Mensaje de salida": f"La película {pelicula.capitalize()} fue estrenada el año {año} y obtuvo un score de {popularidad}"}

#cambiar el nombre del decorador
@app.get("/titulo_de_la_filmacion")
async def votos_titulo(titulo: str) -> dict:
    pelicula = titulo.lower().strip()

    if not pelicula:  # Verifica si la cadena está vacía
        return {"error": "Has ingresado una cadena vacía. Por favor ingresa un título válido."}

    if not all(caracter.isalnum() or caracter.isspace() for caracter in pelicula):
        return {"error": "Por favor ingresa un título sin símbolos."}

    if pelicula not in movies_df['title'].values:
        return {"error": f"La película {titulo.capitalize()} no existe o no se encuentra dentro de la base de datos."}

    # Obtiene los datos de la película
    datos_pelicula = movies_df.loc[movies_df['title'] == pelicula]

    # Verifica si se encontró la película y obtén el número de votos
    if not datos_pelicula.empty:
        cantidad_votos = datos_pelicula['vote_count'].iloc[0]
        if cantidad_votos < 2000:
            return {"error": f"La película {titulo.capitalize()} tiene muy pocas votaciones para ser considerada."}

        media_votos = datos_pelicula['vote_average'].iloc[0]
        return {"Mensaje de salida": f"La película {pelicula.capitalize()} tiene un total de {cantidad_votos} y una media de valoración de {media_votos}"}

    return {"error": "No se encontraron datos para la película solicitada."}

# Prueba la función
print(votos_titulo('toy story'))

"""
def get_actor( nombre_actor ): Se ingresa el nombre de un actor que se encuentre dentro de un dataset debiendo 
devolver el éxito del mismo medido a través del retorno. Además, la cantidad de películas que en las que ha 
participado y el promedio de retorno. La definición no deberá considerar directores.
"""

@app.get('/get_actor')
# porque nunique y no count
async def obtener_actor(actor: str) -> dict:

    actor = actor.lower().strip()

    if not actor:  # Verifica si la cadena está vacía
        return {"error": "Has ingresado una cadena vacía. Por favor ingresa un nombre  y apellido de actor válido."}

    #ver si sirve
    if not all(char.isalpha() or char.isspace() for char in actor):
        raise HTTPException(status_code=400, detail="El nombre del actor debe contener solo letras y/o espacios.")

    if actor not in cast['name'].values:
        return {"error": f"El nombre {actor.capitalize()} no es un actor o no se encuentra dentro de la base de datos."}

    ids_peliculas_actor = cast.loc[cast['name'] == actor]['id_credits'].unique()

    cantidad_peliculas = len(ids_peliculas_actor)

    ganancia = round(movies_df[movies_df['id'].isin(ids_peliculas_actor)]['return'].sum(), 2)

    promedio_ganancia = round(movies_df[movies_df['id'].isin(ids_peliculas_actor)]['revenue'].mean(), 2)
    
    return {"Mensaje de salida": f"El actor {actor.capitalize()} ha participado en {cantidad_peliculas} películas, el mismo ha conseguido un retorno de {ganancia} con un promedio de {promedio_ganancia} por filmación"}


# Arreglar el mensaje de salida
@app.get('/get_director')
async def obtener_director(director: str) -> dict:
    director = director.lower().strip()

    if not director:  # Verifica si la cadena está vacía
        return {"Error": "Has ingresado una cadena vacía. Por favor ingresa un nombre y apellido de director válido."}

    if not all(char.isalpha() or char.isspace() for char in director):
        raise HTTPException(status_code=400, detail="El nombre del director debe contener solo letras y/o espacios.")

    # Verifica si el director está en el DataFrame crew
    if director not in crew['name'].str.lower().values:
        return {"error": f"El nombre {director.capitalize()} no es un director o no se encuentra dentro de la base de datos."}

    # Obtiene los IDs de las películas del director
    ids_director = crew.loc[crew['name'].str.lower() == director, 'id_credits'].unique()

    # Filtra las películas usando los IDs del director
    peliculas_df = movies_df[movies_df['id'].isin(ids_director)]

    # Selecciona y renombra las columnas deseadas
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

    return {
        "Nombre Director": director,
        "Retorno Total": retorno_total,
        "Peliculas": peliculas
    }


@app.get('/recomendacion/{titulo}')
async def recomendar_pelicula(titulo_pelicula: str) ->dict:

    indice = modelo_prediccion.index[modelo_prediccion['title'].str.lower() == titulo_pelicula.lower()].tolist()
    if not indice:
        return {"Error": "Película no encontrada"}

    puntajes_similitud = cosine_similarity(matriz_reducida[indice[0]].reshape(1, -1), matriz_reducida)

    puntajes_similitud = sorted(enumerate(puntajes_similitud[0]), key=lambda x: x[1], reverse=True)

    indices_peliculas = [i[0] for i in puntajes_similitud[1:6]]
    recomendaciones = modelo_prediccion['title'].iloc[indices_peliculas].tolist()

    return {"Recomendaciones": recomendaciones}
