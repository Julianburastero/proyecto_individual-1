#modificar lo que se pueda

import re
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag

def tokenizar(valor: str) -> str:

    valor = re.sub("[^a-zA-Z]", " ", str(valor))
    

    valor = re.sub(r'\s+', ' ', valor).strip()


    tokens = word_tokenize(valor)


    tokens_etiquetados = pos_tag(tokens)


    tokens_filtrados = [token for token, pos in tokens_etiquetados if pos not in ['NNP', 'NNPS']]


    tokens = [token.lower() for token in tokens_filtrados]


    stop_words = set(stopwords.words('english'))
    tokens_filtrados = [token for token in tokens if token not in stop_words]    

    lemmatizer = WordNetLemmatizer()
    tokens_lemmatizados = [lemmatizer.lemmatize(token) for token in tokens_filtrados]


    return ' '.join(tokens_lemmatizados)
    