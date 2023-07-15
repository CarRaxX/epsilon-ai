# Imports
from Config.dependencies import logging, Queue, json, List, colored, Llama
from Config.configuration import global_config


def open_ai_model_generate_text(request_text_queue: Queue, response_text_queue: Queue, open_ai_key: str, open_ai_model: str, open_ai_model_personality: str, open_ai_model_temperature: float, open_ai_model_max_tokens: int, open_ai_model_top_p: int, open_ai_model_frequency_penalty: int, open_ai_model_presence_penalty: int) -> None:
    # Importamos la libreria de la API de OpenAI
    from Config.dependencies import openai
    # Iniciando generado de texto del ML
    logging.info("Epsilon está pensando la respuesta...")
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
    print(colored('### Epsilon: ' + message_response, 'magenta'))
    # Limpiamos el mensaje
    message_response = ""
    
def void_model_generate_text(request_text_queue: Queue, response_text_queue: Queue) -> None:
    # Iniciando generado de texto del ML
    logging.info("Epsilon está pensando la respuesta...")
    # Obtenemos el mensaje que se le hace al modelo  de la cola
    request_text_queue.get()
    # Generamos una cola de texto e introducimos la respuesta
    message_response = 'Hola, este es un mensaje por defecto'
    response_text_queue.put(message_response)
    print(colored('### Epsilon: ' + message_response, 'magenta'))
    # Limpiamos el mensaje
    message_response = ""

def llama_cpp_model_generate_text(request_text_queue: Queue, response_text_queue: Queue, llama_cpp_model: Llama, llama_cpp_instruccion: str, llama_cpp_chat_example: str, llama_cpp_max_predict_tokens: int, llama_cpp_temperature: float, llama_cpp_top_p: float, llama_cpp_stop: List[str], llama_cpp_repeat_penalty: float, llama_cpp_top_k: float) -> None:
    # Iniciando generado de texto del ML
    logging.info("Epsilon está pensando la respuesta...")
    # Obtenemos el mensaje que se le hace al modelo de la cola
    message = request_text_queue.get()
    # Generamos la entrada de texto del modelo (Instruccion + Chat de ejemplo + mensaje)
    input = llama_cpp_instruccion + llama_cpp_chat_example + "### " + global_config['human_interpreter'] + ": " + message + "\n" + "### Epsilon: "
    logging.info("Input:\n" + input)
    # Otenemos el modelo
    llm = llama_cpp_model
    # Insertamos los parametros del modelo para la salida
    output = llm(
    input,
    max_tokens=llama_cpp_max_predict_tokens,
    temperature=llama_cpp_temperature,
    top_p=llama_cpp_top_p,
    echo=True,
    stop=llama_cpp_stop,
    repeat_penalty=llama_cpp_repeat_penalty,
    top_k=llama_cpp_top_k,
    )
    # Generamos una cola de texto e introducimos la respuesta
    message_response = output
    response_text_queue.put(message_response)
    print(colored(f'### Epsilon: {message_response}', 'magenta'))
    # Limpiamos el mensaje
    message_response = ""