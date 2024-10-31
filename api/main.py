from fastapi import FastAPI
import pandas as pd

movies_df = pd.read_parquet('b:/proyecto_individual_1/data_post_etl/movies/movies_dataset_etl.parquet')

app = FastAPI()

meses = {
            'enero': 1, 'febrero': 2, 'marzo':3, 'abril':4, 'mayo': 5, 'junio':6, 'julio':7, 
            'agosto':8, 'septiembre':9, 'octubre':10, 'noviembre': 11, 'diciembre': 12
}

@app.get("/")
def read_root():
    return {"Hello": "World"}