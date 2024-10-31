import ast
import pandas as pd
from pandas import isna  

"""Esta función se encarga de tomar una columan de un DataFrame y convertir sus 
valores str a diccionarios y listas. En caso de ser un NaN lo convierte a None"""

def convertir_list_dict(valor_columna: any) -> dict | list | None:
    """
    Parametros
    ----------
    valor_columna: posee una columna con valores str y/o nan a convertir
    """
    
    #covierte los valores NaN a None
    if isna(valor_columna):
        return None

    #En caso de ser un str transforma transforma a dict o list dependiendo el caso
    if isinstance(valor_columna, str):
        try:
            return ast.literal_eval(valor_columna)
        except (ValueError, SyntaxError):
            return valor_columna

    #Devuelve la columna transformada
    return valor_columna

