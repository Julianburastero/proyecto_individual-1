import re

"""
Normaliza el texto dado eliminando caracteres no alfabéticos, 
convirtiéndolo a minúsculas y eliminando espacios adicionales.
"""

def normalizar(valor: str) -> str:
    """
    Parámetros
    ----------
    valor: str: La cadena de texto que se desea normalizar.
    """
    
    # Convertimos el texto a minúsculas para estandarizarlo:
    valor = valor.lower()  

    # Reemplazamos múltiples espacios en blanco por uno solo:
    valor = re.sub(r'\s+', ' ', valor)  

    # Eliminamos todos los caracteres que no son palabras ni espacios:
    valor = re.sub(r'[^\w\s]', '', valor) 

    # Eliminamos espacios en blanco al principio y al final de la cadena y la devolvemos:
    return valor.strip()  
