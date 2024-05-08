import mysql.connector

config = {
  'user': 'root',
  'password': 'root',
  'host': 'localhost',
  'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
  'database': 'tweets',
  'raise_on_warnings': True
}

# Establecer la conexión
cnx = mysql.connector.connect(**config)

# Crear un cursor para ejecutar consultas
cursor = cnx.cursor(dictionary=True)

# Ejecutar la consulta
cursor.execute('SELECT `id`, `name` FROM `test`')

# Obtener los resultados de la consulta
results = cursor.fetchall()

# Iterar sobre los resultados e imprimir cada fila
for row in results:
    id = row['id']
    title = row['name']
    print('%s | %s' % (id, title))

# Cerrar el cursor y la conexión
cursor.close()
cnx.close()