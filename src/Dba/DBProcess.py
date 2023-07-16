# Imports
from Config.dependencies import logging, pymongo, datetime
# Config
from Config.configuration import config_dba

## DB Config
def init_db() -> None:
    logging.info('Inicializando BBDD...')
    # Establecer la conexión con el servidor MongoDB
    client = pymongo.MongoClient(config_dba['dbHsot'])
    # Establecer la BBDD
    db = client[config_dba['dbName']]
    # Establecer la Colección
    collection = db[config_dba['collection_ctx_chat_name']]

    # Crear un índice en el campo "fecha"
    collection.create_index("fecha")

    # Cerrar la conexión al finalizar la operación
    client.close()


# Función que inserta la conversación entre Humano y Epsilon

def insert_chat(human_name: str, human_message: str, ai_name: str, ai_message) -> None:
    logging.info('Insertando chat en la BBDD...')
    # Establecer la conexión con el servidor MongoDB
    client = pymongo.MongoClient(config_dba['dbHsot'])
    # Establecemos la BBDD
    db = client[config_dba['dbName']]
    # Establecemos la Colección
    collection = db[config_dba['collection_ctx_chat_name']]
    # Creamos la petición de insert con los datos de entrada y fecha
    # Obtener la fecha actual
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    chat = {"human": human_name, "human_message": human_message, "AI": ai_name, "AI_message": ai_message, "fecha": fecha_actual}
    collection.insert_one(chat)
    logging.info('Datos insertados')
    # Cerrar la conexión al finalizar la operacion
    client.close()
    
def obtener_registros_rango_fecha(fecha_inicio: str, fecha_fin: str) -> list:
    logging.info('Obteniendo registros en BBDD del dia ' + fecha_inicio + ' al dia ' + fecha_fin + '...')
    # Convertir las fechas de entrada al formato datetime
    fecha_inicio_dt = datetime.strptime(fecha_inicio, "%Y-%m-%d")
    fecha_fin_dt = datetime.strptime(fecha_fin, "%Y-%m-%d")

    # Establecer la conexión con el servidor MongoDB
    client = pymongo.MongoClient(config_dba['dbHsot'])
    # Establecer la BBDD
    db = client[config_dba['dbName']]
    # Establecer la Colección
    collection = db[config_dba['collection_ctx_chat_name']]

    # Construir la consulta para obtener los registros en el rango de fechas
    consulta = {
        "fecha": {
            "$gte": fecha_inicio_dt,
            "$lt": fecha_fin_dt
        }
    }

    # Ejecutar la consulta y obtener los registros
    registros = list(collection.find(consulta))

    # Cerrar la conexión al finalizar la operación
    client.close()

    # Devolver la lista de registros
    return registros