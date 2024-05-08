import mysql.connector
import pandas as pd
from datetime import datetime
from deep_translator import GoogleTranslator

# Configuración de la conexión a la base de datos MySQL
config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'tweets',
    'raise_on_warnings': True,
    'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock'  
}

# Establecer la conexión
cnx = mysql.connector.connect(**config)

# Crear un cursor para ejecutar consultas
cursor = cnx.cursor()

# Lista de tablas en la base de datos
tables = ['usuarios', 'tweets', 'hashtags', 'tweet_hashtags']  # Asegúrate de incluir todas tus tablas

# Eliminar todos los datos de cada tabla
for table in tables:
    delete_query = f"DELETE FROM {table}"
    cursor.execute(delete_query)

# Confirmar la eliminación
cnx.commit()

# Cargar datos desde el archivo JSON
file_path = 'tweets_extraction.json'
data = pd.read_json(file_path)

# Procesar los datos para cada tabla

# Usuarios
usuarios = pd.DataFrame(data['usuario'].unique(), columns=['nombre'])
cantidad = 0
for _, row in usuarios.iterrows():
    nombre = row['nombre']
    cursor.execute("INSERT INTO usuarios (nombre) VALUES (%s)", (nombre,))
    cantidad += 1
cnx.commit()
print("\nUsuarios insertados: ", cantidad) 

# Obtener usuarios con IDs asignados
cursor.execute("SELECT * FROM usuarios")
usuarios_con_ids = cursor.fetchall()
usuario_id_map = {nombre: id for id, nombre in usuarios_con_ids}




# Tweets
tweets = data[['id', 'texto', 'fecha', 'retweets', 'favoritos', 'usuario']]
duplicates = 0
cantidad = 0
for _, row in tweets.iterrows():
    id = row['id']
    texto = row['texto']
    fecha_str = row['fecha']
    fecha = datetime.strptime(fecha_str, '%Y-%m-%dT%H:%M:%S.%fZ').date() 
    retweets = row['retweets']
    favoritos = row['favoritos']
    nombre_usuario = row['usuario']
    usuario_id = usuario_id_map[nombre_usuario]
    try:
        cursor.execute("INSERT INTO tweets (id, texto, fecha, retweets, favoritos, usuario) VALUES (%s, %s, %s, %s, %s, %s)",
                       (id, texto, fecha, retweets, favoritos, usuario_id))
        cantidad += 1
    except mysql.connector.Error as err:
        if err.errno == 1062:
             duplicates += 1
        else:
            print("Error al insertar tweet:",id, err) 

print("\nTweets insertados: ", cantidad) 
print("Tweets duplicados no insertados: ", duplicates) 
cnx.commit()


# Insertar hashtags
hashtags = pd.DataFrame(data['hashtags'].explode().dropna().unique(), columns=['hashtag'])
duplicates = 0
cantidad = 0
for _, row in hashtags.iterrows():
    hashtag = row['hashtag']
    hashtag = hashtag.rstrip(',.;"')
    try:
        cursor.execute("INSERT INTO hashtags (hashtag) VALUES (%s)", (hashtag,))
        cantidad += 1
    except mysql.connector.Error as err:
        if err.errno == 1062:
             duplicates += 1
        else:
            print("Error al insertar hashtag:", err) 

print("\nHashtags insertados: ", cantidad)
print("Hashtags duplicados no insertados: ", duplicates) 
cnx.commit()

# Recuperar hashtags con IDs asignados
cursor.execute("SELECT * FROM hashtags")
hashtags_con_ids = cursor.fetchall()
hashtag_id_map = {hashtag: id for id, hashtag in hashtags_con_ids}

# Tweet_hashtags
tweet_hashtags = data.explode('hashtags')
tweet_hashtags['hashtags'] = tweet_hashtags['hashtags'].apply(lambda x: x.rstrip(',.;"') if isinstance(x, str) else x)
tweet_hashtags['tweet_id'] = tweet_hashtags['id'].astype(str)
tweet_hashtags['hashtag_id'] = tweet_hashtags['hashtags'].map(hashtag_id_map)
tweet_hashtags = tweet_hashtags[['tweet_id', 'hashtag_id']].dropna()
cantidad = 0
for _, row in tweet_hashtags.iterrows():
    tweet_id = row['tweet_id']
    hashtag_id = row['hashtag_id']
    try:
        cursor.execute("INSERT INTO tweet_hashtags (tweet_id, hashtag_id) VALUES (%s, %s)", (tweet_id, hashtag_id))
        cantidad += 1
    except mysql.connector.Error as err:
        if err.errno == 1062:
             duplicates += 1
        else:
            print("Error al insertar Hashtags_Tweets:", err) 

print("\nHashtags_Tweets insertados: ", cantidad)
print("Hashtags_Tweets duplicados no insertados: ", duplicates) 
cnx.commit()

# Cerrar el cursor y la conexión
cursor.close()
cnx.close()

print("\nDatos cargados exitosamente en la base de datos.")
