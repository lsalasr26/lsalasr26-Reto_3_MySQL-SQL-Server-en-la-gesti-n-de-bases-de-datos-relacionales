import mysql.connector

# Configuración de la conexión a la base de datos MySQL
config = {
        'user': 'ubc6zjphktsuzwvu',
    'password': 'igyeilZNL0493zP9dFlp',
    'host': 'bzulyivg8aiy5kattkta-mysql.services.clever-cloud.com',
    'database': 'bzulyivg8aiy5kattkta',
    'port': 3306
}

# Establecer la conexión
cnx = mysql.connector.connect(**config)

# Crear un cursor para ejecutar consultas
cursor = cnx.cursor()

# Lista de tablas en la base de datos
tables = ['tweet_hashtags', 'tweets', 'hashtags', 'usuarios']  # Asegúrate de incluir todas tus tablas

# Eliminar todos los datos de cada tabla
for table in tables:
    delete_query = f"DELETE FROM {table}"
    cursor.execute(delete_query)

# Confirmar la eliminación
cnx.commit()

# Cerrar el cursor y la conexión
cursor.close()
cnx.close()

print("Todos los datos han sido eliminados de las tablas.")
