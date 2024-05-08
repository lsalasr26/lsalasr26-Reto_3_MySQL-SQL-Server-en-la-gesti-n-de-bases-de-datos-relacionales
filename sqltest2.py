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
cursor = cnx.cursor()

# Insertar un nuevo registro en la tabla 'test'
new_record = ("INSERT INTO test "
              "(id, name) "
              "VALUES (%s, %s)")
record_data = (8, 9)
cursor.execute(new_record, record_data)

# Confirmar la transacción
cnx.commit()

# Cerrar el cursor y la conexión
cursor.close()
cnx.close()
