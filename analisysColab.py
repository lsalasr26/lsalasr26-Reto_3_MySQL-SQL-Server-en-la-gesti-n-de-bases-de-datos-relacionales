import mysql.connector
import pandas as pd
from textblob import TextBlob
import nltk
from textblob.exceptions import NotTranslated

# Asegurar la descarga de stopwords y corpora necesarios
nltk.download('punkt')

# Configuración de la conexión a la base de datos
config = {
    'user': 'ubc6zjphktsuzwvu',
    'password': 'igyeilZNL0493zP9dFlp',
    'host': 'bzulyivg8aiy5kattkta-mysql.services.clever-cloud.com',
    'database': 'bzulyivg8aiy5kattkta',
    'port': 3306
}

# Función de análisis de sentimientos
def get_sentiment(text):
    try:
        analysis = TextBlob(text).translate(from_lang='es', to='en')
        # print("Inglés")
    except NotTranslated:
        analysis = TextBlob(text)
        #print("Español")
    return 'positivo' if analysis.sentiment.polarity > 0 else 'negativo' if analysis.sentiment.polarity < 0 else 'neutral'

# Función para determinar el valor de 'feeling' basado en 'sentimiento'
def update_feeling(sentiment):
    return 1 if sentiment == 'positivo' else -1 if sentiment == 'negativo' else 0 if sentiment == 'neutral' else -2

# Conectar a la base de datos y ejecutar consulta
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = "SELECT id, texto FROM tweets WHERE feeling = -2"
    cursor.execute(query)
    tweets = cursor.fetchall()
except Exception as e:
    print("Error durante la conexión o consulta:", e)
finally:
    cursor.close()
    cnx.close()

# Procesar cada tweet y actualizar la base de datos
try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    for tweet_id, texto in tweets:
        sentimiento = get_sentiment(texto)
        nuevo_feeling = update_feeling(sentimiento)
        update_query = "UPDATE tweets SET feeling = %s WHERE id = %s"
        cursor.execute(update_query, (nuevo_feeling, tweet_id))
        cnx.commit()

except Exception as e:
    print("Error durante la actualización de la base de datos:", e)
finally:
    cursor.close()
    cnx.close()

print("Actualización completada.")
