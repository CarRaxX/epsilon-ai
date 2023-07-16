# Imports
from Config.dependencies import logging, Queue, json, List, colored, Llama, unidecode, re
from Config.configuration import global_config


def open_ai_model_generate_text(request_text_queue: Queue, response_text_queue: Queue, open_ai_key: str, open_ai_model: str, open_ai_model_personality: str, open_ai_model_temperature: float, open_ai_model_max_tokens: int, open_ai_model_top_p: int, open_ai_model_frequency_penalty: int, open_ai_model_presence_penalty: int) -> None:
    # Importamos la libreria de la API de OpenAI
    from Config.dependencies import openai
    # Iniciando generado de texto del ML
    logging.info("" + global_config['ai_interpreter'] + " está pensando la respuesta...")
    # Obtenemos el mensaje que se le hace al modelo de la cola
    message = request_text_queue.get()
    # Generamos la petición con la clave a la API de OpenAI
    openai.api_key = (open_ai_key)

    response = openai.Completion.create(
        model=open_ai_model,
        prompt=open_ai_model_personality + "\n\n#########\n" + message + "\n#########\n",
        temperature=open_ai_model_temperature,
        max_tokens=open_ai_model_max_tokens,
        top_p=open_ai_model_top_p,
        frequency_penalty=open_ai_model_frequency_penalty,
        presence_penalty=open_ai_model_presence_penalty
    )
    # Dividimos los fragmentos de la respuesta
    json_object = json.loads(str(response))
    # Generamos una cola de texto e introducimos la respuesta
    message_response = json_object['choices'][0]['text']
    message_response = str(message_response).rstrip('\n')
    response_text_queue.put(message_response)
    print(colored('### ' + global_config['ai_interpreter'] + ': ' + message_response, 'magenta'))
    # Limpiamos el mensaje
    message_response = ""
    
def void_model_generate_text(request_text_queue: Queue, response_text_queue: Queue) -> None:
    # Iniciando generado de texto del ML
    logging.info("" + global_config['ai_interpreter'] + " está pensando la respuesta...")
    # Obtenemos el mensaje que se le hace al modelo  de la cola
    request_text_queue.get()
    # Generamos una cola de texto e introducimos la respuesta
    message_response = 'Hola, este es un mensaje por defecto'
    response_text_queue.put(message_response)
    print(colored('### ' + global_config['ai_interpreter'] + ': ' + message_response, 'magenta'))
    # Limpiamos el mensaje
    message_response = ""

def normalize_text(text):
    # Normalizar caracteres especiales
    normalized_text = unidecode.unidecode(text)
    # Filtrar caracteres no controlados
    filtered_text = re.sub(r"[^\w\s#.,!<>:'?]", "", normalized_text)
    return filtered_text

def llama_cpp_model_generate_text(request_text_queue: Queue, response_text_queue: Queue, llama_cpp_model: Llama, llama_cpp_epsilon_personality: str, llama_cpp_epsilon_init_chat: str, llama_cpp_max_predict_tokens: int, llama_cpp_temperature: float, llama_cpp_top_p: float, llama_cpp_stop: List[str], llama_cpp_repeat_penalty: float, llama_cpp_top_k: float) -> None:
    # Iniciando generado de texto del ML
    logging.info("" + global_config['ai_interpreter'] + " está pensando la respuesta...")
    # Obtenemos el mensaje que se le hace al modelo de la cola
    message = request_text_queue.get()
    # Generamos la entrada de texto del modelo (Instruccion + Chat de ejemplo + mensaje)
    # TODO - Obtener el ctx_chat (Contexto del chat) de la BBDD desde una fecha anterior a hoy (concatenar con llama_cpp_epsilon_init_chat)
    ctx_chat = llama_cpp_epsilon_init_chat + ""
    # Se define la personalidad de Epsilon
    input = "" + global_config['ai_interpreter'] + "'s Persona: " + llama_cpp_epsilon_personality + "<START>\n" + ctx_chat + global_config['human_interpreter'] + ": " + message + "\n" + "" + global_config['ai_interpreter'] + ":"
    # Normalizamos el texto
    normalized_input = normalize_text(input)
    #logging.info("Input:\n" + normalized_input)
    # Otenemos el modelo
    llm = llama_cpp_model
    # Insertamos los parametros del modelo para la salida
    output = llm(
    normalized_input,
    max_tokens=llama_cpp_max_predict_tokens,
    temperature=llama_cpp_temperature,
    top_p=llama_cpp_top_p,
    repeat_penalty=llama_cpp_repeat_penalty,
    top_k=llama_cpp_top_k,
    stop=llama_cpp_stop,
    echo=False
    )
    # Generamos una cola de texto e introducimos la respuesta
    # print(f'Output: {output}')
    data = output
    message_response = data['choices'][0]['text']
        
    response_text_queue.put(message_response)
    print(colored(f'' + global_config['ai_interpreter'] + ':{message_response}', 'magenta'))
    # Limpiamos el mensaje
    message_response = ""