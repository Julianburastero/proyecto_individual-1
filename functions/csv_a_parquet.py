from pandas import DataFrame
import pandas as pd

"""Esta función se encarga de transformar archivos a parquet, 
especificametne archivos csv"""

def convertidor_parquet(csv: str, parquet: str) -> DataFrame:
    
    """
    Parametros:
    -----------
    #csv: toma la ruta csv a transformar
    #parquet: toma la ruta parquet transformada
    """
    
    #Leemos el archivo csv alojandolo en un df
    df = pd.read_csv(csv)

    #Generamos la transformación csv a parquet
    df.to_parquet(parquet, engine='pyarrow', index = False)

    #Retornamos en forma de dataframe
    return df