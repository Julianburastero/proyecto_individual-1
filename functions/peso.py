
import pandas as pd

"""
    Concatena el contenido de 'overview' con el de 'columna_texto', 
    multiplicando el contenido de esta última para darle más peso.
"""

def combinar_peso(fila, columna_texto: str, peso: int) -> str:

    """
    Parámetros:
    ----------
    fila (pandas.Series): Fila actual con el 'overview' y la columna a ponderar.
    columna_texto (str): Nombre de la columna cuyo contenido se ponderará.
    peso (int): Número de veces que se repetirá el texto para aumentar su peso.
    """

    # Extraemos el texto de 'overview' y de la columna especificada:
    overview = fila['overview']
    texto = fila[columna_texto]
    
    # Si el texto de la columna es NaN, devolvemos solo el resumen original:
    if pd.isna(texto):
        return overview
    
    # Generamos el texto ponderado repitiendo 'texto' el número de veces indicado en 'peso':
    texto_ponderado = ' '.join([texto] * peso)

    # Concatenamos el resumen con el texto ponderado y lo devuelvemos
    return f"{overview} {texto_ponderado}"