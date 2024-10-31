import pandas as pd

def convertir_float(df, columna):
    """
    Esta función toma una columna de un DataFrame y la convierte a tipo float.
    Si hay valores que no se pueden convertir, los transforma a NaN.

    Parámetros
    ----------
    df: DataFrame en el que se realizará la conversión.
    columna: Nombre de la columna a ser transformada.
    """

    try:
        df[columna] = df[columna].astype(float)
    except ValueError:
        print(f"Warning: La conversión de la columna '{columna}' a float falló debido a valores no convertibles. Se intentará con 'pd.to_numeric'.")
        df[columna] = pd.to_numeric(df[columna], errors='coerce')

    return df