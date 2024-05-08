import mysql.connector
import pandas as pd
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from textblob import TextBlob
import nltk
from deep_translator import GoogleTranslator

# Asegurar la descarga de stopwords
nltk.download('stopwords')

try:
    # Configuración de la conexión a la base de datos
    config = {
        'user': 'root',
        'password': 'root',
        'host': 'localhost',
        'database': 'tweets',
        'raise_on_warnings': True,
        'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock'
    }

    # Conectar a la base de datos
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Consulta para seleccionar los tweets
    query = "SELECT id, texto, fecha, retweets, favoritos, usuario FROM tweets"
    cursor.execute(query)

    # Crear un DataFrame con los datos de los tweets
    columns = ['id', 'texto', 'fecha', 'retweets', 'favoritos', 'usuario']
    tweets_df = pd.DataFrame(cursor.fetchall(), columns=columns)
finally:
    # Cerrar el cursor y la conexión
    cursor.close()
    cnx.close()

# Carga de stopwords y configuración de stemmer
#stop_words = set(stopwords.words('spanish'))  
#stemmer = SnowballStemmer('spanish')

# Funciones de preprocesamiento y análisis de sentimientos
#def clean_text(text):
 #   text = re.sub(r"http\S+|@\S+|#\S+", "", text)
 #   text = re.sub(r"[^A-Za-záéíóúñÁÉÍÓÚÑüÜ ]", "", text)
 #   text = re.sub(r"\b\d+\b", "", text)
 #   words = text.split()
 #   return " ".join([stemmer.stem(word) for word in words if word not in stop_words])
    #return " ".join([word for word in words if word.lower() not in stop_words])



def get_sentiment(text):
    analysis = TextBlob(text).translate(from_lang='es', to= 'en')
    return 'positivo' if analysis.sentiment.polarity > 0 else 'negativo' if analysis.sentiment.polarity < 0 else 'neutral'

# Aplicación de funciones al DataFrame
#tweets_df['texto_limpio'] = tweets_df['texto'].apply(clean_text)
tweets_df['sentimiento'] = tweets_df['texto'].apply(get_sentiment)

# Mostrar las primeras filas del DataFrame procesado
print(tweets_df.head())

# Conteo de sentimientos
sentiment_counts = tweets_df['sentimiento'].value_counts()
print("\nConteo de Sentimientos:")
print(sentiment_counts)