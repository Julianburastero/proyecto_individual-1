import pandas as pd
from pandas import DataFrame

"""Esta función se encarga de crear una nueva tabla a partir de desanidación y la 
consecuente normalización de los datos de una columna dada. Los valores de dicha 
columna en el DataFrame original serán reemplazados por un ID que los represente.
"""

def desanidar_columna(df: DataFrame,
                    columna: str,
                    nombre_nueva_tabla: str,
                    indice_increment:int=0) -> DataFrame:

    """
    Parametros
    ----------
    df: Este parametro se encarga de tomar el dataframe original para trabajar 
    con el
    columna: Esta linea toma la columna del dataset original que se quiere 
    desanidar
    nombre_nueva_tabla: Este es el nombre arbitario seleccionado que va a 
    representar a la nueva tabla
    indice_increment: Es un paramatero opcional que elije a partir de que numero
    se iniciara el incremento del indice.
    """

    # Se aloja el DataFrame en la variable
    df_original = df
    
    # Se crea un id único en el DataFrame original
    df_original[f'{columna}_id'] = df_original.index + indice_increment

    # Se útiliza la función explode para desanidar la columna
    df_original_desanidado = df_original.explode(columna)

    # Se utiliza la función json_normalize para normalizar los datos de la columna
    # Y se crea la nueva tabla
    nombre_nueva_tabla = pd.json_normalize(df_original_desanidado[columna])

    # Se crea una nueva columna en la tabla nueva con un id relacionado al id
    # previamente creado en el DataFrame orginal
    nombre_nueva_tabla[f'{columna}_id'] = df_original_desanidado[f'{columna}_id'].values

    #Se retorna la tabla nueva
    return nombre_nueva_tabla

