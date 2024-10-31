from fastapi import FastAPI
import pandas as pd

movies_df = pd.read_parquet('data_post_etl/movies/movies_dataset_etl.parquet')

app = FastAPI()

meses = {
            'enero': 1, 'febrero': 2, 'marzo':3, 'abril':4, 'mayo': 5, 'junio':6, 'julio':7, 
            'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre': 11, 'diciembre': 12
}

@app.get("/")
def read_root():
    return {"Hola": "Mundo"}

@app.get("/cantidad_filmaciones_mes")
def cantidad_filmaciones_mes(mes: str) -> dict:
    
    if not mes.isalpha() or mes not in meses:
        return {"error": "Por favor, ingresa un mes en español válido."}
    
    mes = mes.strip().lower()

    mes_numero = meses[mes]

    cantidad_filamaciones = movies_df[movies_df['release_date'].dt.month == mes_numero]
    
    if cantidad_filamaciones.empty:
        return {"message": f"No hay filmaciones para el mes de {mes}."}

    return {"cantidad": f"{cantidad_filmaciones} películas fueron estrenadas en los meses de {mes.capitalize()}"}

