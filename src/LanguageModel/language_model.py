# Imports
from Config.dependencies import logging, Queue, json, List, colored, Llama, unidecode, re, timedelta, datetime
from Config.configuration import global_config, config_dba
from Dba.DBProcess import *
    
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

def normalize_input_text(input_text) -> str:
    # Filtrar caracteres no controlados
    normalized_input = re.sub(r"[^\w\s#.,!¡*<>ñ:'¿?]", "", input_text)
    return normalized_input

def normalize_output_text(output_text) -> str:
    # Eliminar caracteres especiales salvo la "ñ"
    filtered_text = re.sub(r"[^\w\sñ,.!¡:'*¿?]", "", output_text)
    # Eliminar espacios excesivos al inicio y final de la cadena
    trimmed_text = filtered_text.strip()
    # Eliminar espacios excesivos en el medio de la cadena
    normalized_output = re.sub(r"\s+", " ", trimmed_text)
    
    return normalized_output
    
def get_ctx_chat(llama_cpp_epsilon_init_chat: str, ctx_days: int) -> str:
    logging.info(f"Obteniendo el contexto del chat de hace {ctx_days} días")
    
    # Llamar a la función para eliminar registros antiguos si es necesario
    eliminar_registros_antiguos(max_registros=config_dba['max_ctx_registers'])  # Ajusta el número máximo de registros permitidos
    # Utiliza fecha_inicio y fecha_fin en tu función obtener_registros_rango_fecha() para obtener los registros dentro de ese período
    registros = obtener_registros()

    # Concatenar los registros con el valor de llama_cpp_epsilon_init_chat
    ctx_chat = llama_cpp_epsilon_init_chat
    for registro in registros:
        ctx_chat += registro["human"] + ": " + registro["human_message"] + "\n"
        ctx_chat += registro["ai"] + ": " + registro["ai_message"] + "\n"

    return ctx_chat

def llama_cpp_model_generate_text(request_text_queue: Queue, response_text_queue: Queue, llama_cpp_model: Llama, llama_cpp_epsilon_personality: str, llama_cpp_epsilon_init_chat: str, llama_cpp_epsilon_ctx_days: int, llama_cpp_max_predict_tokens: int, llama_cpp_temperature: float, llama_cpp_top_p: float, llama_cpp_stop: List[str], llama_cpp_repeat_penalty: float, llama_cpp_top_k: float) -> None:
    # Iniciando generado de texto del ML
    logging.info("" + global_config['ai_interpreter'] + " está pensando la respuesta...")
    # Obtenemos el mensaje que se le hace al modelo de la cola
    message = request_text_queue.get()
    # Generamos la entrada de texto del modelo (Instruccion + Chat de ejemplo + mensaje)
    # Obtenemos el conexto completo de la BBDD
    ctx_chat = get_ctx_chat(llama_cpp_epsilon_init_chat, llama_cpp_epsilon_ctx_days)
    # Se define la personalidad de Epsilon
    input = "" + global_config['ai_interpreter'] + "'s Persona: " + llama_cpp_epsilon_personality + "<START>\n" + ctx_chat + global_config['human_interpreter'] + ": " + message + "\n" + "" + global_config['ai_interpreter'] + ":"
    # Normalizamos el texto
    normalized_input = normalize_input_text(input)
    logging.info("Input:\n" + normalized_input)
    # Otenemos el modelo
    llm = llama_cpp_model
    # Insertamos los parametros del modelo para la salida
    output = llm(
    normalized_input,
    max_tokens=llama_cpp_max_predict_tokens,
    #temperature=llama_cpp_temperature,
    #top_p=llama_cpp_top_p,
    #repeat_penalty=llama_cpp_repeat_penalty,
    #top_k=llama_cpp_top_k,
    stop=llama_cpp_stop,
    echo=False
    )
    # Generamos una cola de texto e introducimos la respuesta
    # print(f'Output: {output}')
    data = output
    message_response = data['choices'][0]['text']
    ai_message = normalize_output_text(message_response)
    # Guardamos el mensaje en la cola de respuesta de texto
    response_text_queue.put(ai_message)
    # Añadimos el contexto del chat a la BBDD
    insert_chat(global_config['human_interpreter'], message, global_config['ai_interpreter'], ai_message)
    print(colored(f"{global_config['ai_interpreter']}: {ai_message}", "magenta"))
    # Limpiamos el mensaje
    message_response = ""