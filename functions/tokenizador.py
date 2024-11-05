import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

"""
La función tokenizar procesa una cadena de texto eliminando caracteres no 
alfabéticos y espacios extra, tokenizando el texto, etiquetando los tokens, 
filtrando nombres propios y stopwords, y lematizando las palabras restantes. 
Devuelve el texto limpio y preparado para análisis de lenguaje natural.
"""

def tokenizar(texto: str) -> str:
    """
    Parámetros
    ----------
    texto: El único parámetro es texto, el cual espera una cadena para generar los
    siguientes cambios:
    """

    # Eliminamos caracteres no alfabéticos y convertimos el texto a cadena:
    texto_limpio = re.sub("[^a-zA-Z]", " ", str(texto))
    
    # Reemplazamos múltiples espacios en blanco por uno solo y eliminamos espacios al principio y al final:
    texto_limpio = re.sub(r'\s+', ' ', texto_limpio).strip()

    # Tokenizamos el texto en palabras individuales:
    lista_tokens = word_tokenize(texto_limpio)

    # Etiquetamos cada token con su parte del habla (POS tagging):
    tokens_etiquetados = pos_tag(lista_tokens)

    # Convertimos los tokens a minúsculas y filtramos los nombres propios (NNP, NNPS):
    tokens_filtrados = [token.lower() for token, pos in tokens_etiquetados if pos not in ['NNP', 'NNPS']]

    # Obtenemos la lista de stopwords en inglés:
    palabras_vacias = set(stopwords.words('english'))

    # Filtramos los tokens, eliminando las stopwords:
    tokens_finales = [token for token in tokens_filtrados if token not in palabras_vacias]    

    # Creamos un lematizador para reducir las palabras a su forma base:
    lemmatizer = WordNetLemmatizer()

    # Aplicamos lematización a los tokens restantes:
    tokens_lemmatizados = [lemmatizer.lemmatize(token) for token in tokens_finales]

    # Unimos los tokens lematizados en una cadena y la devolvemos:
    return ' '.join(tokens_lemmatizados)




