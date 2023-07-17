# Imports
from Config.dependencies import logging, pymongo, datetime, timedelta
# Config
from Config.configuration import config_dba

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
    
    # Eliminar los registros antiguos
    result = collection.delete_many({})
    logging.info(f"Registros eliminados: {result.deleted_count}")

    # Cerrar la conexión al finalizar la operación
    client.close()
    
def exit_db() -> None:
    logging.info('Cerrando BBDD...')
    # Establecer la conexión con el servidor MongoDB
    client = pymongo.MongoClient(config_dba['dbHsot'])
    # Establecer la BBDD
    db = client[config_dba['dbName']]
    # Establecer la Colección
    collection = db[config_dba['collection_ctx_chat_name']]

    # Borrar todos los registros de la colección
    collection.delete_many({})

    # Cerrar la conexión al finalizar la operación
    client.close()

def verificar_ultimos_registros(collection, ai_message):
    # Construir la consulta para buscar los últimos 3 registros
    consulta_ultimos_registros = {"ai_message": ai_message}
    
    # Buscar los últimos 3 registros que coincidan con el mensaje AI
    registros_ultimos = collection.find(consulta_ultimos_registros).sort("fecha", pymongo.DESCENDING).limit(3)
    
    # Verificar si todos los últimos 3 registros coinciden con el mensaje AI
    registros_encontrados = list(registros_ultimos)
    if len(registros_encontrados) < 3:
        return False

    for registro in registros_encontrados:
        if registro["ai_message"] != ai_message:
            return False
    
    return True

def insert_chat(human_name: str, human_message: str, ai_name: str, ai_message: str) -> None:
    logging.info('Insertando chat en la BBDD...')
    # Establecer la conexión con el servidor MongoDB
    client = pymongo.MongoClient(config_dba['dbHsot'])
    # Establecemos la BBDD
    db = client[config_dba['dbName']]
    # Establecemos la Colección
    collection = db[config_dba['collection_ctx_chat_name']]
    
    # Verificar si todos los últimos registros coinciden con el mensaje AI
    if verificar_ultimos_registros(collection, ai_message):
        logging.info('El mensaje AI ya existe en los últimos 3 registros de la BBDD. No se realizará la inserción.')
        # Cerrar la conexión al finalizar la operación
        client.close()
        return
    
    # Crear el nuevo registro
    fecha_actual = datetime.now()
    chat = {
        "human": human_name,
        "human_message": human_message,
        "ai": ai_name,
        "ai_message": ai_message,
        "fecha": fecha_actual
    }
    
    # Insertar el nuevo registro en la colección
    collection.insert_one(chat)
    
    logging.info('Datos insertados correctamente.')
    # Cerrar la conexión al finalizar la operación
    client.close()


    
def eliminar_registros_antiguos(max_registros: int) -> None:
    logging.info(f"Comprobando registros en la BBDD...")

    # Establecer la conexión con el servidor MongoDB
    client = pymongo.MongoClient(config_dba['dbHsot'])
    # Establecer la BBDD
    db = client[config_dba['dbName']]
    # Establecer la Colección
    collection = db[config_dba['collection_ctx_chat_name']]

    # Contar el número de registros en la colección
    num_registros = collection.count_documents({})

    # Calcular la mitad de los registros actuales
    mitad_registros = num_registros // 2

    # Comprobar si el número de registros iguala o supera el máximo
    if num_registros >= max_registros:
        # Obtener los registros más antiguos hasta la mitad
        registros_eliminar = collection.find({}).sort("fecha", pymongo.ASCENDING).limit(mitad_registros)

        # Eliminar los registros más antiguos
        for registro in registros_eliminar:
            collection.delete_one({"_id": registro["_id"]})

        logging.info(f"{mitad_registros} registros eliminados de la BBDD.")
    else:
        logging.info(f"No es necesario eliminar registros. Número actual de registros: {num_registros}")

    # Cerrar la conexión al finalizar la operación
    client.close()
    
def obtener_registros() -> list:
    logging.info(f"Obteniendo registros en BBDD...")

    # Establecer la conexión con el servidor MongoDB
    client = pymongo.MongoClient(config_dba['dbHsot'])
    # Establecer la BBDD
    db = client[config_dba['dbName']]
    # Establecer la Colección
    collection = db[config_dba['collection_ctx_chat_name']]

    # Ejecutar la consulta y obtener los registros en orden ascendente por fecha
    registros = list(collection.find({}).sort("fecha", pymongo.ASCENDING))

    # Cerrar la conexión al finalizar la operación
    client.close()

    # Devolver la lista de registros
    return registros