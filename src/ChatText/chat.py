# Imports
from Config.dependencies import logging, Queue
from Config.configuration import global_config

def get_input_text(request_text_queue: Queue) -> None:
    # Generamos la entrada de texto
    logging.info('' + global_config['ai_interpreter'] + ' está esperando tu petición por texto...')
    while True:
        request = input('Inserte su petición: ')
        if request.strip():  # Si la entrada no está vacía después de eliminar espacios en blanco
            request_text_queue.put(request)  # Guardamos la entrada de texto en la cola de peticiones
            break  # Salir del bucle si la entrada es válida
        else:
            logging.info('La peticion está vacía. Inténtalo de nuevo.')  # Mostrar un mensaje de error si la entrada está vacía
    
