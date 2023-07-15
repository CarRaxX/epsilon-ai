# Imports
from Config.dependencies import logging
# Config
from Config.configuration import *
from Config.models import *
# .py Methods
from VoiceToText.transcript import *
from ChatText.chat import *
from LanguageModel.check_request import *
from LanguageModel.language_model import *

# Opción de chat de texto


def text_chat_option() -> None:
    # Realizamos la configuración inicial
    logging.info('Configurando Epsilon para el chat por texto...')
    # Inicializamos la configuración...
    # Cola de petición por Texto
    request_text_queue = global_config['request_text_queue']
    # Cola de respuesta por Texto
    response_text_queue = global_config['response_text_queue']
    # Cola de respuesta por Audio
    response_audio_queue = global_config['response_audio_queue']
    # Seleccionamos el modelo a usar y lo cargamos en memoria
    # TODO
    logging.info('Se va a hablar con Epsilon vía chat de texto')
    # Mientras no se cumpla la condicion de salida seguimos en el bucle
    while not global_config['is_exit_request']:
        # 1.Obtenemos el texto de entrada
        get_input_text(request_text_queue)
        # 2.Comprobamos la petición
        # Comprobamos la petición y Cambiamos los estados
        check_request(
            request_text_queue, config_check['keywords'], config_check['stop_keywords'])
        # Si se da una petición, se formula al modelo de lenguaje
        if global_config['is_epsilon_request']:
            # 4.Formulamos la petición al Modelo de Lenguaje y obtenemos su respuesta
            #
            # open_ai_model_generate_text(request_text_queue, response_text_queue, config_open_ai_generate_text['open_ai_key'], config_open_ai_generate_text['open_ai_model'], config_open_ai_generate_text['open_ai_model_personality'], config_open_ai_generate_text[
            #    'open_ai_model_temperature'], config_open_ai_generate_text['open_ai_model_max_tokens'], config_open_ai_generate_text['open_ai_model_top_p'], config_open_ai_generate_text['open_ai_model_frequency_penalty'], config_open_ai_generate_text['open_ai_model_presence_penalty'])
            #
            # void_model_generate_text(request_text_queue, response_text_queue)
            llama_cpp_model_generate_text(request_text_queue, response_text_queue, config_llama_cpp_generate_text['llama_cpp_model_path'], config_llama_cpp_generate_text['llama_cpp_instruccion'], config_llama_cpp_generate_text['llama_cpp_chat_example'], config_llama_cpp_generate_text[
                                          'llama_cpp_max_predict_tokens'], config_llama_cpp_generate_text['llama_cpp_temperature'], config_llama_cpp_generate_text['llama_cpp_top_p'], config_llama_cpp_generate_text['llama_cpp_stop'], config_llama_cpp_generate_text['llama_cpp_repeat_penalty'], config_llama_cpp_generate_text['llama_cpp_top_k'])

    exit_option()

# Opción de chat de voz


def voice_chat_option() -> None:
    # Realizamos la configuración inicial
    logging.info('Configurando Epsilon para el chat por voz...')
    # Inicializamos la configuración...
    # Cola de petición por Audio
    request_audio_queue = global_config['request_audio_queue']
    # Cola de petición por Texto
    request_text_queue = global_config['request_text_queue']
    # Cola de respuesta por Texto
    response_text_queue = global_config['response_text_queue']
    # Cola de respuesta por Audio
    response_audio_queue = global_config['response_audio_queue']
    # Cargamos el modelo de Wishper para escuchar
    whisper_model = load_whisper_model(
        config_transcribe['type_model'])  # Modelo de Wishper
    logging.info('Se va a hablar con Epsilon vía chat de voz')
    # Mientras no se cumpla la condicion de salida seguimos en el bucle
    while not global_config['is_exit_request']:
        # 1.Grabamos
        # Obtenemos la cola de petición de texto
        record_audio(request_audio_queue, config_record['energy'], config_record['pause_threshold'],
                     config_record['dynamic_energy'], config_record['save_file'], config_record['file_path'], config_record['file_name'])
        # 2.Transcribimos
        # Obtenemos la cola de petición de audio
        transcribe_audio_queue(request_audio_queue, request_text_queue,
                               global_config['request_text_queue'], whisper_model, config_transcribe['language'])
        # 3.Comprobamos la petición
        # Comprobamos la petición y Cambiamos los estados
        check_request(
            request_text_queue, config_check['keywords'], config_check['stop_keywords'])
        # Si se da una petición, se formula al modelo de lenguaje
        if global_config['is_epsilon_request']:
            # 4.Formulamos la petición al Modelo de Lenguaje y obtenemos su respuesta
            open_ai_model_generate_text(request_text_queue, response_text_queue, config_open_ai_generate_text['open_ai_key'], config_open_ai_generate_text['open_ai_model'], config_open_ai_generate_text['open_ai_model_personality'], config_open_ai_generate_text[
                'open_ai_model_temperature'], config_open_ai_generate_text['open_ai_model_max_tokens'], config_open_ai_generate_text['open_ai_model_top_p'], config_open_ai_generate_text['open_ai_model_frequency_penalty'], config_open_ai_generate_text['open_ai_model_presence_penalty'])

    exit_option()

# Opción de chat de salir


def exit_option() -> None:
    logging.info('Epsilon se va a dormir.')
    exit()


def init_config() -> None:
    logging.info('Configurando ')


# Opciones asignadas a números
options = {
    "1": text_chat_option,
    "2": voice_chat_option,
    "3": exit_option
}

# Menú de opciones


def options_menu() -> None:
    while True:
        logging.info("Menú de opciones de Epsilon:")
        logging.info("1. Chat por texto")
        logging.info("2. Chat por voz")
        logging.info("3. Salir")
        # Opción del usuario
        option = input("Inserte la opción a ejecutar: ")
        # Realizamos la acción en función de las acciones asignadas a los numeros
        action = options.get(option)
        if action:
            # Ejecutamos la opción seleccionada
            action()
        else:
            logging.info(
                "Opción incorrecta, seleccione una con las teclas 1, 2 o 3.")


# Main
if __name__ == '__main__':
    logging.info("¡Epsilon está despierta!")
    options_menu()
