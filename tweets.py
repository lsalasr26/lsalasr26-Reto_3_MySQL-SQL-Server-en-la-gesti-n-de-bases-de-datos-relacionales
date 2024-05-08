import json

# Abre el archivo JSON y carga los datos
with open('tweets_extraction.json', 'r') as file:
    data = json.load(file)


for index, item in enumerate(data):
    if index < 3:  
        print(f"Tweet {index+1} keys:")
        estructura_datos = {}
        for field, value in item.items():
            if isinstance(value, list): 
                if value:  
                    estructura_datos[field] = [type(element).__name__ for element in value]
                else:
                    estructura_datos[field] = 'Empty List'
            else:
                estructura_datos[field] = type(value).__name__
        print(estructura_datos)
