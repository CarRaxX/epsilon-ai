# Imports
from Config.dependencies import logging, unidecode, re, Queue, List, colored
# Config
from Config.configuration import global_config

# Función que revisa el texto transcrito


def check_request(request_text_queue: Queue, keywords: List[str] = ['epsilon'], stop_keywords: List[str] = ['adios']) -> None:
    # Reseteamos el tipo de petición de Epsilon
    global_config['is_epsilon_request'] = False
    # Obtenemos el siguiente fragmento de texto de la cola
    result_text = request_text_queue.get()
    print(colored('### ' + global_config['human_interpreter'] +': ' + result_text, 'blue'))
    # Formateamos el texto
    # logging.info('Formateando el texto...')
    format_result_text = format_text(result_text)
    
    # Comprobamos si se ha dicho una palabra que detenga la aplicación
    for stop_keyword in stop_keywords:
        if stop_keyword in format_result_text:
            # Es una petición de salida
            global_config['is_exit_request'] = True
                    
    # Aplicamos la petición en base al resultado de la comprobación
    if global_config['is_exit_request']:
       # Si se dicen el conjunto de palabras que detienen el proceso, se para
       logging.info(
           f"Se ha dicho una palabra clave de detención")
       # Se realiza la petición de despedida
       logging.info(
           f"Se ha realizado una petición a Epsilon con el texto de despedida: \"{result_text}\"")
       # Realizar petición...
       request_text_queue.put(result_text)
       global_config['is_epsilon_request'] = True
       # Paramos la app
    else:
        # Se realiza una petición normal al modelo de Lenguaje Epsilon
        logging.info(
            f"Se ha realizado una petición a Epsilon con el texto: \'{result_text}\'")
        # Realizar petición...
        request_text_queue.put(result_text)
        global_config['is_epsilon_request'] = True
            
    # Limpiamos el mensaje
    result_text = ""
    format_result_text = ""

# Función que formatea un texto a minusculas, sin acentos y sin puntuación


def format_text(text: str) -> str:
    # Eliminamos los signos de puntuación
    text = re.sub(r'[^\w\s]', '', text)
    # Convertimos el texto a minúsculas
    text = text.lower()
    # Eliminamos los acentos
    text = unidecode.unidecode(text)
    # Eliminamos el primer espacio sobrante si se trata de un espacio
    if (text[1] == ' '):
        text = text[1:]

    return text
